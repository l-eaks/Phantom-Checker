import requests
import threading

class UsernameChecker:
    def __init__(self, num_threads):
        self.available_usernames = []
        self.lock = threading.Lock()
        self.num_threads = num_threads

    def check_username_availability(self, username):
        url = f"https://api.phantom.app/user/v1/profiles/{username}"
        response = requests.get(url)

        if response.status_code == 404:
            with self.lock:
                self.available_usernames.append(username) 

    def run_check(self, usernames):
        threads = []
        
        for username in usernames:
            while threading.active_count() > self.num_threads:
                continue 

            thread = threading.Thread(target=self.check_username_availability, args=(username,))
            threads.append(thread)
            thread.start()  

        for thread in threads:
            thread.join()

def main():
    with open('usernames.txt', 'r') as file:
        usernames = [line.strip() for line in file if line.strip()] 

    num_threads = int(input("Enter the number of threads to use: "))
    
    checker = UsernameChecker(num_threads)

    checker.run_check(usernames)

    with open('available.txt', 'w') as file:
        for username in checker.available_usernames:
            file.write(username + '\n')

    print(f"Available usernames have been written to available.txt.")

if __name__ == "__main__":
    main()
