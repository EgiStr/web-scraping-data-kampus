from collectData import Request


if __name__ == '__main__':
    # ask input for keyword SBMPTN or SNMPTN
    keyword = int(input("Masukkan kata kunci SBMPTN(1) atau SNMPTN(0): "))
    # ask input for keyword jurusan until user input 'q' and convert to list
    jurusan = []
    while True:
        jurusan_input = input("( 'q' to stop ) Masukkan jurusan:  ")
        if jurusan_input == 'q':
            break
        jurusan.append(jurusan_input)
        
    
    # ask input for keyword name_file
    name_file = input("Masukkan nama file: ")
    # create object Request
    request = Request(keyword, jurusan, name_file)
    # get request
    request.start()
