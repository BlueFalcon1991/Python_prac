import os
import heapq

def find_largest_files(start_path='C:\\', top_n=10):
    file_sizes = []

    for foldername, subfolders, filenames in os.walk(start_path):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            try:
                size = os.path.getsize(filepath)
                heapq.heappush(file_sizes, (size, filepath))
                if len(file_sizes) > top_n:
                    heapq.heappop(file_sizes)
            except (OSError, PermissionError):
                continue

    largest_files = sorted(file_sizes, reverse=True)

    print(f"\nTop {top_n} largest files in '{start_path}':\n")
    for size, filepath in largest_files:
        print(f"{size / (1024 * 1024):.2f} MB - {filepath}")

if __name__ == "__main__":
    find_largest_files('C:\\', top_n=10)