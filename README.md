# Simple Text Editor Using Ropes Data Structure
 This is the final project for the course Data Structures II - CS 201, offered in Spring 2023 by Habib University. It is a simple Text Editor created from scratch using Python and Tkinter implemented on Ropes Data Structure. 

## About Ropes
A Rope data structure is a tree data structure which is used to store or manipulate large strings in a more efficient manner. It allows for operations like insertion, deletion, search and random access to be executed faster and much more efficiently in comparison to a traditional String.

This data structure is widely used by softwares such as text editors like Sublime, email systems like Gmail and text buffers to handle large strings efficiently.

![image](https://user-images.githubusercontent.com/44427180/234474825-50e35162-c68c-441f-908a-b6aebd455a21.png)

## Create Rope Object
```rope = Rope("Hello, world! ")```

## Search
```searchResult = rope.search(rope.root, "ello", 0)```
```print(searchResult)```

## Insertion
```rope.insert(rope.root, "Yousuf", 14)```

## Deletion
```rope.delete(rope.root, 0, 14)```

## Replace
```rope.replace(rope.root, "Yousuf", "Uyghur")```

```print(rope)```
```print(rope.root.size)```