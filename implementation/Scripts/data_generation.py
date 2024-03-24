import random


def main():
    output = []
    for i in range(10):
        temp = [str(i) for j in range(500)]
        output += temp

    random.shuffle(output)

    to_write = [output[i:i + 100] for i in range(0, len(output), 100)]
    for i in range(len(to_write)):
        with open(f'labels_{i}.txt', 'w') as f:
            f.write(",".join(to_write[i]))


if __name__ == '__main__':
    main()
