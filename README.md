# ProgramingLanguage_08
PL Assignment #8: Cute17 Project

PL Assignment #8: Cute17 Project
������ �ΰ��� : 2017-05-11 (��)
Program Upload ������ : �� �����ۿ� ���� �ٸ�
����
�� ���� ������ ������ �� Cute 17������ ���� ���α׷��� �Է��ϸ� ����� ����ϴ� ��������
�͸� ���� �� �����϶�
Project ����
�Ʒ��� ���� 2���� item���� ������. �Ʒ� ������ ���� �����ϸ�, �� ������ ���� ������ ����
�Ѵ�. ���� ������ ��� �� ���� ���� ���� �д㵵 ��Ȯ�ϰ� �Ǿ�� �Ѵ�.
Item 1. ���α׷��� interpretation ȯ�� ����,
Item 2. ������ ���ε� ó��: define������ ������ �����ϰ� ����� �� �ֵ��� �Ѵ�.
�Լ��� ���ε� ó��: define������ �Լ��� �����ϰ� ����� �� �ֵ��� �����Ѵ�.
(�Լ��� �Լ��� ���ڷ� �Ѿ� �� �� �־�� �Ѵ�. ? SSR���)
����)
- ������ define ���� ���� �����Ѵ�
��) test case 1, 2 �� �� ����
- �̸����� �Լ��� ���Ǵ�
(lambda (parameter_list) (optional_definition_of_local_vars) (function_body) )
�� ���� �������� �����Ѵ�. (optional_definition_of_local_vars) �� ��� �ȴ�
��) test case 8�� �� ����
- �Լ��� �̸��� ������ �Ǵ� ���
define ���� ������ ���� �����ϵ��� define���� �̸����� �Լ��� ������ �� �ִ�.
��) test case 12 �� �� ����
- �Լ��� �̸��� ���� �ٸ� �Լ��� ���ڷ� ���� �� �� �ִ�.
��) test case 18, 19�� �� ����
- �Լ� ������ �Լ��� ���ǵ� �� �ִ�.
lambda���� define �� Ȱ���ؼ� (optional_definition_of_local_vars) ���ο��� ����
��) test case 20 �� �� ����
���� ������ ���� ���� 1��
�������� �ּ��� ������ ��� ���� ���ԵǾ� ����.
Project TEST Case
1. (define a 1)
a ;; 1
2. (define b ��(1 2 3))
b ;; ��(1 2 3)
3. (define c (- 5 2))
C ;; 3
4. (define d ��(+ 2 3))
D ;;`(+ 2 3)
5. (define test b)
test ;;��(1 2 3) (2��)
6. (+ a 3) ;;4
7. (define a 2) ;; �տ� a�� ���ǵ� �Ŀ� ���� ����
(* a 4) ;;8
8. ((lambda (x) (* x -2)) 3) ;;-6
9. ((lambda (x) (/ x 2)) a) ;;1(2��)
10. ((lambda (x y) (* x y)) 3 5) ;;15(2��)
11. ((lambda (x y) (* x y)) a 5) ;;10(2��)
12. (define plus1 (lambda (x) (+ x 1))) ;; ���� �Լ� ����
(plus1 3) ;;4 (3��)
13. (define mul1 (lambda (x) (* x a))) ;; ���� �Լ� ����, ���� ���� ����
(mul1 a) ;;4 (3��)
14. (define plus2
(lambda (x) (+ (plus1 x) 1))) ;;�Լ� ������ ���� �Լ� ȣ�� ����
(plus2 4) ;; 6 (3��)
15. (define plus3
(lambda (x) (+ (plus1 x) a))) ;;�Լ� ������ ���� �Լ� ȣ�� ����, ���� ���� ����
(plus3 a) ;; 5 (3��)
16. (define mul2
(lambda (x) (* (plus1 x) -2)))
(mul2 7) ;; -16 (3��)
17. (define lastitem
(lambda (ls)
(cond ((null? (cdr ls)) (car ls))
(#T (lastitem (cdr ls)))))) ;;Recursion ���� (6��)
18. (define square (lambda (x) (* x x)))
(define yourfunc (lambda (x func) (func x))
(yourfunc 3 square) ;;�Լ����� �Լ��� ���ڷ� ��밡�� (4��)
19. (define square (lambda (x) (* x x)))
(define mul_two (lambda (x) (* 2 x)))
(define new_fun (lambda (fun1 fun2 x) (fun2 (fun1 x))))
(new_fun square mul_two 10) ;; (4��)
20. (define cube
(lambda (n) (define sqrt (lambda (n) (* n n)))
(* (sqrt n) n))) ;;Nested �Լ� ���� (3��)
(sqrt 4) ;; ����(����ó���� �� �ʿ�� ����) (3��)