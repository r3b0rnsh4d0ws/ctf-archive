# K17 2026 - java-notes (web, medium)

## Challenge
- **Description:** "I heard Java's the hot new language on the block. It's certainly making my CPU hot!"
- **Instance:** `https://8080-6daf060f725749ea9895764c63bd6a7a.sbx.secso.cc`
- **Files:** Maven project (Main.java, pom.xml, Dockerfile)
- **Flag:** `K17{i_am_java_ONE_with_java!!!!oashd8aghrdfo8aehFIOEASDJFNLC}`

## Vulnerability
Java deserialization (`ObjectInputStream.readObject()` on user base64) with
commons-collections 3.2.1 on JDK 11. RCE is blind (Runtime.exec async), but the
restore handler's `sessionJson()` calls `String.valueOf(note)` -> `toString()` on
each note, turning a `TiedMapEntry` note into an output channel.

## Exploit
Craft a `com.k17.javanotes.Main$Session` (nested class name!) whose notes list
contains a `TiedMapEntry` wrapping a `LazyMap` with a file-read transformer chain:

```
ConstantTransformer(Scanner.class)
  -> InstantiateTransformer([File.class], [File("/flag.txt")])
  -> InvokerTransformer("nextLine")
```

`sessionJson` -> `TiedMapEntry.toString()` -> `LazyMap.get("foo")` -> chain reads
/flag.txt -> flag returned as the note text in the JSON response.

## Key gotchas
- Server class is `com.k17.javanotes.Main$Session` (nested -> `$`), not
  `com.k17.javanotes.Session` -> decode a real /api/export token to confirm.
- Session constructor is package-private -> builder must be in the same package.
- `Runtime.exec` is async -> `sleep 5` gives no timing delay; don't build a timing
  oracle. Use the toString() file-read trick instead.

## Flag
```
K17{i_am_java_ONE_with_java!!!!oashd8aghrdfo8aehFIOEASDJFNLC}
```

## Lessons
- Java deserialization chains don't have to exec: `InstantiateTransformer` +
  `InvokerTransformer` build arbitrary objects (Scanner(File).nextLine()) and
  return output through toString().
- Blind RCE: find toString() call sites on deserialized objects as output channels.
- Decode a legit token from the live service for exact class names / serialVersionUID.