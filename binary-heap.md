#Binary Heap

Binary Heap is a binary tree with two additional constraints.

  1. ***shape property***:
    the tree nearly complete binary tree. i.e all levels are completely filled except possibly the lowest, which is filled from left up to a point
  2. ***heap property***:
    the nodes are either >=(max-heap) or <=(min-heap) each of its children


Heaps are commonly implemented using arrays with `A[0]` as root.
```java
int left(int i){
    return 2*i+1;
}

int right(int i){
    return 2*i+2;
}

int parent(int i){
    return Math.floor((i-1)/2);
}

int height(int n){
    return Math.floor(log2(n));
}
```
in max-heap:

* $A[parent[i]]\geq A[i]$
* largest element is at root

in min-heap:

* $A[parent[i]]\leq A[i]$
* smallest element is at root

root is said to be at level 0  
\#elements at level $L = 2^L$  
total #elements from root to level $L = 2^0+2^1+2^2+…+2^L = 2^{L+1}-1$

height of n element heap = $\lfloor(log_2n)\rfloor$  
min #elements in heap of height h = ?  
max #elements in heap of height h = ?

##Addition
* add new element to end of heap
* keep moving it up until it is larger than its parent

```java
void add(int a[], int size, int v){
    a[size] = v;
    siftUp(a, size);
}

void siftUp(int a[], int i){
    while(i>0){
        int ip = parent(i);
        if(a[ip]<a[i]){
            swap(a, ip, i);
            i = ip;
        }else
            return;
    }
}
```
>Note: `siftUp` assumes `a[0…i-1]` is heap

Running Time: $O(\log_2n)$

##Deletion
   * replace element to be deleted with last element of heap
   * keep moving down until it is smaller than its children

```java
void delete(int a[], int size, int i){
    a[i] = a[size-1];
    siftDown(a i, size-1);
}

void siftDown(int a[], int size, int i){
    while(left(i)<size){ // i is not leaf
        int max = i;

        int left = left(i);
        if(a[left]>a[max])
            max = left;

        int right = right(i);
        if(right<size && a[right]>a[max]) // right child exists and it is bigger
            max = right;

        if(max!=root){
            swap(a, i, max);
            i = max;
        }else
            break;
    }
}
```

   * `siftDown` assumes that, binary trees rooted at `left(i)` and `right(i)` are max-heaps but `a[i]` may be smaller than its children, thus violating max-heap property
   * In `siftDown`, `a[i]` flow-down so that, subtree rooted at `a[i]` becomes a max-heap
   * notice that `siftDown` is actually merging two heaps

Running Time: $O(\log_2n)$

##Replace

if new element is less than element being replaced do `siftDown`, otherwise do `siftUp`

```java
// replace a[i] with v
void replace(int a[], int size, int i, int v){
    int oldV = a[i];
    a[i] = v;
    if(v<oldV)
        siftDown(a, end, i);
    else if(v>oldV)
        siftUp(a, i);
    return oldV;
}
```
Running Time: $O(\log_2n)$

##Heapify

array elements $\lfloor length[A]/2\rfloor \cdots1$ are all leaves of the tree.  
these leaves can be treated as each is one-element heap.

```java
void heapify(int a[], int size){
    for(int i=size/2-1; i>=0; i--) // from index of last parent node
        siftDown(a, size, i);
}
```

Running Time: $O(n)$

alternatively `heapify` can be implemented using `siftUp`:

```java
void heapify(int a[], int size){
    for(int i=1; i<size; i++)
        siftUp(a, i);
}
```
Running Time: $O(n\log_2n)$

## Finding the `k` smallest of `N` items, where $k<<N$?

```java
void findLargest(int a[], int k){
    heapify(a, k); // create max-heap with first k elements
    for(int i=k+1; i<a.length; i++){
        if(a[i]<a[0])
            replace(a, k, 0); // replace with root
    }
}
```

Running Time: $O(N)+O(N\log_2k)$

##Heap Sort

```java
void heapSort(int a[], int count){
    heapify(a, count);

    int end = count-1;
    while(end>0){
        swap(a[0], a[end]);
        end--;
        siftDown(a, 0, end);
    }
}
```

Runing Time: $O(n\log_2n)$

>NOTE: heap sort is not stable  

##Merge K Sorted Linked Lists [@][1]

extend `merge` of `merge-sort` to `k` sorted lists  
to find min of all list heads use min-heap

```java
void merge(Node lists[]){
    if(lists.length==0)
        return null;
    else if(lists.length==1)
        return lists[0];

    int heapSize = lists.length;

    // compare values of head nodes
    minHeapify(lists, lists.length);

    Node head=null, tail=null;
    while(heapSize>1){
        Node min = lists[0];
        if(min.next==null)
            remove(lists, heapSize--, 0);
        else
            replace(lists, heapSize, 0, min.next);

        if(head==null)
            head = tail = min;
        else
            tail = min;
    }

    tail.next = lists[0];
}
```
minHeapify takes $O(k)$  
while loop runs `n` times where `n`=sum of sorted list sizes  
each while loop takes $log_2k$ times

Running Time: $O(k)+O(n\log_2k)=O(n\log_2k)$

##Sort k-sorted array [@][2]

in ***k-sorted array***, each element is at most `k` positions away from its target position  
i.e `i` the element in sorted array, should is in `a[i-k…i+k]`

if we use Insertion Sort, the inner loop runs at most k times.  
so running-time: $O(nk)$

we can use selection sort, where min element is selected repeatedly.  
in k-sorted array, the min element must be in first `k+1` positions.  
so use min-heap, to effectively find min

```java
void sort(int a[], int k){
   int b[k+1];
   copy a[0…k+1] to b
   heapify(b, k+1);

   for(int i=0,j=k+1; i<a.length; i++,j++){
       a[i] = b[0];
       if(j<a.length)
           replace(b, k+1, 0, a[j]);
       else
           remove(b, k+a.length-j, 0);
   }
}
```
`heapify` takes $O(k)$  
`n` heap operations each taking $O(\log_2k)$  
so running-time: $O(n\log_2k)$  
auxiliary-space: $O(k)$

##Median of Integer Stream [@][3]

***median*** is the middle element in an odd length sorted array, and in the even case it’s the average of the middle elements

Given a stream of unsorted integers, find the median element in sorted order at any given time ?

use 2 heaps simultaneously, a max-heap and a min-heap with following invariants

   * **order invariant**
      * max-heap contains the smallest half of the numbers and min-heap contains the largest half
      * So the numbers in max-heap are always less than or equal to the numbers in min-heap
   * **size invariant**
      * \#elements in max-heap is either equal to or `1` more than #elements in the min-heap
      * so if we received `2N` elements(even) up to now, max-heap and min-heap will both contain `N` elements.
      * if we have received `2N+1` elements(odd), max-heap will contain `N+1` and min-heap `N`

```java
double getMedian(int maxHeap[], int minHeap[], int size){
    if(size%2==0)
        return (maxHeap[0]+minHeap[0])/2.0;
    else
        return maxHeap[0];
}

void append(int maxHeap[], int minHeap[], int size, int v){
    if(size%2==0){
        // sizes: N, N
        if(v<=minHeap[0])
            add(maxHeap, size/2, v); // N+1, N
        else{
            add(minHeap, size/2, v); // N, N+1

            // move minHeap root to maxHeap
            add(maxHeap, size/2, minHeap[0]);
            delete(minHeap, (size/2)+1, 0);
        }
    }else{
        // sizes: N+1, N
        if(v>=maxHeap[0])
            add(minHeap, size/2, v);
        else{
            add(maxHeap, (size/2)+1, v); // N+2, N

            // move maxHeap root to minHeap
            add(minHeap, size/2, maxHeap[0]);
            delete(maxHeap, (size/2)+2, 0);
        }
    }
}
```


[1]: http://www.geeksforgeeks.org/merge-k-sorted-arrays/
[2]: http://www.geeksforgeeks.org/nearly-sorted-algorithm/
[3]: http://www.ardendertat.com/2011/11/03/programming-interview-questions-13-median-of-integer-stream/
