#GREP
**G**lobal **R**egular **E**xpression **P**rint

`grep [options] [pattern] [file...]`  

prints all lines in file containing pattern

## Pattern
`.` means any character  
`*` means repetition  
`\` to escape special character  

## Options
`-n` to show line numbers  
`-v` prints lines not containing pattern  
`-r` to search subdirectories recursively  
`-i` to ignore case  
`-c` print only number of lines  
`-l` print only file names  
`-f` to specify file containing pattern. ex: `grep -f patternfile file`
