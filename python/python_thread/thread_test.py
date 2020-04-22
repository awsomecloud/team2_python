import time
import threading
import concurrent.futures

start = time.perf_counter()

#싱글 테스트 시에는 seconds 제거
def do_something(seconds):
    #변수넘기는 스레딩 테스트시
    print(f'Sleep {seconds} second(s)..')
    time.sleep(seconds)
    #싱글 테스트
    # print(f'Sleep {seconds} second(s)..')
    #time.sleep(1)

    #print(f'done sleeping...{seconds}')
    return f'done sleeping...{seconds}'


#싱글로 그냥 돌릴때
#do_something()
#------------------

#스레딩
# t1 = threading.Thread(target=do_something)
# t2 = threading.Thread(target=do_something)
#
# t1.start()
# t2.start()
#
# t1.join()
# t2.join()
#------------------

#반복문으로 스레딩
# threads = []
# for _ in range(10):
#     t = threading.Thread(target=do_something)
#     t.start()
#     threads.append(t)
#
# for thread in threads:
#     thread.join()
#-------------------

#스레딩 시 값 넘기는 방법
# threads = []
# for _ in range(10):
#     t = threading.Thread(target=do_something, args=[1.5])
#     t.start()
#     threads.append(t)
#
# for thread in threads:
#     thread.join()
#--------------------------

#스레딩시 concurrent.futures 사용방법
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:

    #하나씩 지정해서 동시에 돌리기
    # f1 = executor.submit(do_something, 1)
    # f2 = executor.submit(do_something, 1)
    # print(f1.result())
    # print(f2.result())

    #반복문 사용하여 동시에 돌리기
    # results = [executor.submit(do_something, 1) for _ in range(10)]
    # for f in concurrent.futures.as_completed(results):
    #     print(f.result())

    #반복문 사용하여 동시에 돌리기 2 (배열 사용) -- 특징 : 잡아둔 스레드가 각각 종료될때마다 정해둔 다음 작업 인행
    secs = [5, 4, 3, 2, 1]
    results = [executor.submit(do_something, sec) for sec in secs]
    for f in concurrent.futures.as_completed(results):
        print(f.result())

    # 반복문 사용하여 동시에 돌리기 3 (map 사용) -- 특징 : 잡아둔 스레드가 모두 종료 이후 다음 진행
    # secs = [5, 4, 3, 2, 1]
    # results = executor.map(do_something, secs)
    # for result in results:
    #     print(result)

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')