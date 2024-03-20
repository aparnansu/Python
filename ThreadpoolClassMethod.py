import concurrent.futures
import time


class MyClass:
    def __init__(self, name):
        self.name = name

    def my_method(self, seconds):
        print(f"{self.name} starting task, sleeping for {seconds} seconds...")
        time.sleep(seconds)
        print(f"{self.name} task completed after {seconds} seconds.")


def main():
    # Create a thread pool executor with 3 worker threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks to the executor
        tasks = []
        for i in range(1, 4):
            obj = MyClass(f"Thread {i}")
            tasks.append(executor.submit(obj.my_method, i))

        # Wait for all tasks to complete
        concurrent.futures.wait(tasks)


if __name__ == "__main__":
    main()
