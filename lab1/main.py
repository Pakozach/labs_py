from multiprocessing import Process
import time

KEY_SIZE = 8
SORT_TYPE_MERGE = 0
SORT_TYPE_QUICK = 1

def merge_sort(A):
    if len(A) == 0:
        return []
    if len(A) == 1:
        return [0]
    L = merge_sort(A[:len(A) // 2])
    R = merge_sort(A[len(A) // 2:])
    n = m = k = 0
    C = [0] * (len(L) + len(R))
    while n < len(L) and m < len(R):
        if A[L[n]] <= A[R[m] + len(L)]:
            C[k] = L[n]
            n += 1
        else:
            C[k] = R[m] + len(L)
            m += 1
        k += 1
    while n < len(L):
        C[k] = L[n]
        n += 1
        k += 1
    while m < len(R):
        C[k] = R[m] + len(L)
        m += 1
        k += 1
    return C


def swap(obj, i, j):
    obj[j], obj[i] = obj[i], obj[j]


def partition(A, N, low, high):
    p = A[N[high]]
    i = low
    for j in range(low, high):
        if A[N[j]] <= p:
            swap(N, i, j)
            i += 1
    swap(N, i, high)
    return i


def quick_sort_ex(A, N, low, high):
    if low < high:
        p = partition(A, N, low, high)
        quick_sort_ex(A, N, low, p - 1)
        quick_sort_ex(A, N, p + 1, high)


def quick_sort(A):
    N = [i for i in range(len(A))]
    quick_sort_ex(A, N, 0, len(A) - 1)
    return N


def sort(A, sort_type):
    N = []
    if sort_type == SORT_TYPE_MERGE:
        N = merge_sort(A)
    else:
        N = quick_sort(A)
    return N


def read_file_to_list(path, A, lines):
    for line in open(path, 'rt'):
        lines.append(line[:-1])
        A.append(int(line[:KEY_SIZE], 16))


def write_lines_to_file(path, N, lines):
    f = open(path, 'wt')
    for i in range(len(N)):
        f.write(lines[N[i]])
        f.write('\n')


def sort_file(path_in, path_out, sort_type):
    A = []
    lines = []
    read_file_to_list(path_in, A, lines)
    time_start = time.time()
    N = []
    for i in range(1000):
        N = sort(A, sort_type)
    dt = time.time() - time_start
    write_lines_to_file(path_out, N, lines)
    if sort_type == SORT_TYPE_MERGE:
        print(f'Sort MERGE time is {dt}\n')
    else:
        print(f'Sort QUICK time is {dt}\n')


def run(path_in, path_out_quick, path_out_merge):
    procs = []

    proc = Process(target=sort_file, args=(path_in, path_out_merge, SORT_TYPE_MERGE))
    procs.append(proc)

    proc = Process(target=sort_file, args=(path_in, path_out_quick, SORT_TYPE_QUICK))
    procs.append(proc)

    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()


if __name__ == '__main__':
    #   path_in--path_quick_out--path_merge_out
    run('in.txt', 'quick.txt', 'merge.txt')
