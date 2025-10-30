(define (ascending? s) 
        (define (ascendings pre s)
            (if (= (length s) 0)
                #t
                (if (> pre (car s))
                        #f
                        (ascendings (car s) (cdr s)))))
        
            (if (= (length s) 0)
                #t
                (ascendings (car s) (cdr s))))

(define (my-filter pred s) 
    (if (= (length s) 0)
        '()
        (if (pred (car s))
                (cons (car s) (my-filter pred (cdr s)))
                (my-filter pred (cdr s)))))

(define (interleave lst1 lst2)
       (cond
           ((null? lst1) lst2)
           ((null? lst2) lst1)
           (else 
                 (cons (car lst1) (interleave lst2 (cdr lst1))))
            ))

(define (no-repeats s) 
    (if (null? s)
        '()
        (if  (aloned (car s) (cdr s))
        (cons (car s) (no-repeats (cdr s)))
        (no-repeats (cdr s)))
    )
    )

(define (aloned n s)
        (cond
            ((null? s) #t)
            ((= n (car s)) #f)
            (else (aloned n (cdr s))))
)
