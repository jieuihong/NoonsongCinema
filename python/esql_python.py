import pymssql

conn = pymssql.connect(
    server='',
    host='localhost',
    port='',
    database='Noonsong_Cinema',
    charset='utf8')


def check_booked():
    print('\n********** 예매한 영화 확인 **********')
    cursor.execute('select TIMETABLE.DATE, TIMETABLE.TIME, TIMETABLE.MOVIE, TIMETABLE.THEATER, '
                   'THEATER.LOCATION, MOVIE.RUNTIME, RESERVATION.SEAT, TIMETABLE.movieID from RESERVATION '
                   'join TIMETABLE on TIMETABLE.movieID = RESERVATION.movieID '
                   'join MEMBER on MEMBER.ID = RESERVATION.memberID '
                   'join MOVIE on MOVIE.TITLE = TIMETABLE.MOVIE '
                   'join THEATER on TIMETABLE.THEATER = THEATER.THEATER '
                   'where MEMBER.ID = (%s)', user_id)
    row = cursor.fetchone()
    b = 1
    booked = []
    while row:
        print(f'{b}. {row[0].strip()} {row[1].strip()} | {row[2].strip()} | '
              f'{row[3].strip()}({row[4].strip()}) | {row[5].strip()} | 좌석 번호: {row[6]}')

        booked.append(row[7])
        row = cursor.fetchone()
        b += 1

    return b, booked


def delete_booked():
    b, booked = check_booked()

    if len(booked) == 0:
        print("예매 내역이 없습니다")

    else:
        while True:
            want_del = input("삭제를 원하시는 예매 내역의 번호를 입력해주세요\n"
                             "이전 메뉴로 돌아가려면 return을 눌러주세요: ")

            if want_del.isdigit():
                want_del = int(want_del)
                if 1 <= want_del < b:
                    cursor.execute('delete from RESERVATION '
                                   'where movieID = (%s)', booked[want_del - 1])
                    cursor.execute('update MEMBER set HISTORY = HISTORY-1 '
                                   'where ID = (%s)', user_id)
                    update_level()
                    print("내역이 삭제되었습니다.\n")
                else:
                    print('잘못 선택하셨습니다. 다시 입력해주세요\n')
            elif want_del == 'return':
                print('이전 화면으로 돌아갑니다')
                break
            else:
                print("잘못 입력하셨습니다. 다시 입력해주세요\n")
        conn.commit()


def update_level():
    cursor.execute('select HISTORY from MEMBER '
                   'where ID = (%s)', user_id)
    row = cursor.fetchone()
    if row[0] >= 30:
        cursor.execute("update MEMBER set LEVEL='DIAMOND'"
                       "where ID=(%s)", user_id)
    elif 10 <= row[0] < 30:
        cursor.execute("update MEMBER set LEVEL='GOLD'"
                       "where ID=(%s)", user_id)
    elif 5 <= row[0] < 10:
        cursor.execute("update MEMBER set LEVEL='SILVER'"
                       "where ID=(%s)", user_id)
    else:
        cursor.execute("update MEMBER set LEVEL='BRONZE'"
                       "where ID=(%s)", user_id)
    conn.commit()


def login():
    cursor.execute("Select * from MEMBER")
    member = []

    for row in cursor:
        member.append(row[1].strip())

    user_id = input("ID: ")
    user_pw = input("PW: ")

    if user_id not in member:
        user_id, user_pw = new_member()

        if user_id is None:
            login()

    return user_id, user_pw


def new_member():
    join = input("회원 정보가 없습니다. 회원 가입을 하시겠습니까?: \n"
                 "1.네   2.아니오\n"
                 "입력: ")
    if join == '1':
        cursor.execute('select ID from MEMBER')
        row = cursor.fetchone()
        ids = []
        while row:
            ids.append(row[0].strip())
            row = cursor.fetchone()

        while True:
            name = input("이름을 입력해주세요: ")
            new_id = input("ID를 입력해주세요: ")
            new_pw = input("비밀번호를 입력해주세요: ")

            if new_id not in ids:
                cursor.execute("insert into MEMBER (NAME, ID, PW, LEVEL, HISTORY)"
                               "values (%s, %s, %s, %s, %s)", (name, new_id, new_pw, "BRONZE", 0))
                conn.commit()

                return new_id, new_pw

            else:
                print("중복된 아이디입니다. 다시 입력해주세요")

    elif join == '2':
        print("회원가입을 하지 않기로 선택하셨습니다. 로그인 화면으로 돌아갑니다\n")
        return None, None
    else:
        print("잘못 선택하셨습니다. 로그인 화면으로 돌아갑니다.\n")
        return None, None


def currently_showing():
    print("==========현재 상영 중인 영화의 목록입니다.==========")
    # cursor = conn.cursor()
    cursor.execute("select * from MOVIE ")
    row = cursor.fetchone()

    m = 1
    movies = []
    while row:
        print(f"{m}. {row[0].strip()}, {row[4]}\n"
              f"장르: {row[1]}\n"
              f"개봉일: {row[2]}\n"
              f"평점: {row[3]}\n"
              f"감독: {row[5]}\n")
        movies.append(row[0])
        row = cursor.fetchone()
        m += 1

    while True:
        # 영화로 티켓 예매
        want_to = input("상영 시간표를 확인하고 싶은 영화의 번호를 입력해주세요\n"
                        "홈 화면으로 돌아가려면 home을 입력해주세요: ")
        if want_to.isdigit():
            want_to = int(want_to)
            if 1 <= want_to < m:
                selected = movies[want_to - 1]
                print(f"============== <{selected.strip()}>의 상영 시간표입니다 ==============")
                cursor.execute('select * from TIMETABLE '
                               'join THEATER on TIMETABLE.THEATER = THEATER.THEATER '
                               'where TIMETABLE.MOVIE = (%s)', selected)
                row = cursor.fetchone()
                i = 1
                times = []
                while row:
                    print(f"{i}. {row[1]} | {row[2]} | {row[4].strip()} | 잔여 좌석: {row[5]}")
                    times.append(row[0])
                    i += 1
                    row = cursor.fetchone()
                print(" ")
            else:
                print("잘못 입력하셨습니다. 다시 입력해주세요\n")

        elif want_to == 'home':
            print("홈 화면으로 돌아갑니다\n")
            break
        else:
            print("잘못 입력하셨습니다. 다시 입력해주세요\n")


# 날짜로 티켓 예매
def buy_ticket():
    while True:
        cursor.execute('select DISTINCT DATE from TIMETABLE')
        row = cursor.fetchone()
        print("\n========== 예매 가능 날짜 ==========")

        # get all dates from TIMETABLE
        dates = []
        d = 1
        while row:
            print(f"{d}. {row[0]}")
            dates.append(row[0])
            d += 1
            row = cursor.fetchone()

        # get preferred date from user
        preferred_date = input("원하시는 날짜의 번호를 입력해주세요. \n"
                               "홈 화면으로 돌아가고 싶으시다면 home을 입력해주세요: ")
        # if "preferred date" is correct
        if preferred_date.isdigit():
            preferred_date = int(preferred_date)
            if 1 <= preferred_date < d:
                cursor.execute('select * from TIMETABLE '
                               'join THEATER on THEATER.THEATER = TIMETABLE.THEATER '
                               'where DATE=(%s)', dates[preferred_date - 1])

                # print the movies that are on that day
                row = cursor.fetchone()
                mo = 1
                movies = []
                while row:
                    print(
                        f"{mo}. {row[2].strip()} | {row[3].strip()} | {row[4].strip()}, {row[8].strip()} | 여석: {row[5]}")
                    mo += 1
                    movies.append(row[0])
                    row = cursor.fetchone()

                # get the movie that the user wants to watch
                while True:
                    selected_movie = input("원하는 영화의 번호를 입력해주세요\n"
                                           "이전 화면으로 돌아가려면 return을 입력해주세요: ")

                    if selected_movie.isdigit():
                        selected_movie = int(selected_movie)
                        if 1 <= selected_movie < mo:
                            cursor.execute("select THEATER.SEATS, TIMETABLE.REMAINS from TIMETABLE "
                                           "join THEATER on THEATER.THEATER = TIMETABLE.THEATER "
                                           "where TIMETABLE.movieID = (%s)", movies[selected_movie - 1])

                            row = cursor.fetchone()
                            max_seats = row[0]
                            remaining_seats = row[1]

                            # if there aren't any seats left, ask them to choose again
                            if remaining_seats == 0:
                                print("\n해당 영화는 매진되었습니다. 다시 선택해주세요\n")

                            else:
                                # get the movies that the user has booked to prevent them from
                                # buying the same ticket twice
                                cursor.execute('select movieID from RESERVATION '
                                               'join MEMBER on MEMBER.ID = RESERVATION.memberID '
                                               'where MEMBER.ID = (%s)', user_id)

                                row = cursor.fetchone()
                                booked = []
                                while row:
                                    booked.append(row[0])
                                    row = cursor.fetchone()

                                if movies[selected_movie - 1] in booked:
                                    print("이미 예매한 영화입니다. 다시 선택해주세요\n")
                                else:
                                    seat = max_seats - remaining_seats
                                    cursor.execute('insert into RESERVATION (memberID, movieID, SEAT)'
                                                   'values (%s, %s, %d)', (user_id, movies[selected_movie - 1], seat))

                                    cursor.execute('update TIMETABLE set REMAINS = REMAINS-1 where movieID = (%s)',
                                                   movies[selected_movie - 1])

                                    cursor.execute('update MEMBER set HISTORY = HISTORY+1 '
                                                   'where ID = (%s)', user_id)

                                    update_level()
                                    conn.commit()

                                    print('예매가 완료되었습니다. 감사합니다. 홈 화면으로 돌아갑니다.\n')
                                    break
                        else:
                            print("잘못 입력하셨습니다. 다시 입력해주세요\n")

                    elif selected_movie == 'return':
                        print('날짜 선택으로 돌아갑니다\n')
                        break
                    else:
                        print("잘못 입력하셨습니다. 다시 입력해주세요")
            else:
                print("잘못 입력하셨습니다")

        elif preferred_date == 'home':
            print("홈 화면으로 돌아갑니다.")
            break

        else:
            print("잘못 입력하셨습니다")


def my_page():
    while True:
        update_level()

        cursor.execute('select * from MEMBER where ID = (%s)', user_id)
        row = cursor.fetchone()

        member_info = []
        while row:
            member_info.append(row[0].strip())
            member_info.append(row[3].strip())
            row = cursor.fetchone()

        print("\n********** 마이 페이지 **********\n"
              f"{member_info[0]}({user_id})님 등급은 {member_info[1]}입니다\n"
              "1. 정보 수정\n"
              "2. 예매한 영화 확인\n"
              "3. 예매 내역 삭제")
        want = input('원하시는 메뉴의 번호를 입력해주세요\n'
                     '홈 화면으로 돌아가고 싶다면 home을 입력해주세요: ')

        if want == '1':
            while True:
                print('\n1. 이름\n'
                      '2. 비밀번호')
                sel = input("수정할 정보를 선택해주세요: ")

                if sel == '1':
                    new_name = input("새로운 이름을 입력해주세요: ")
                    cursor.execute('update MEMBER set NAME=(%s) where ID=(%s)', (new_name, user_id))
                    conn.commit()

                    print(f"{new_name}(으)로 이름이 변경되었습니다")
                    break
                elif sel == '2':
                    new_pw = input("새로운 비밀번호를 입력해주세요: ")
                    cursor.execute('update MEMBER set PW=(%s) where ID=(%s)', (new_pw, user_id))
                    conn.commit()

                    print("비밀번호가 변경되었습니다")
                    break
                else:
                    print('잘못 입력하셨습니다. 다시 입력해주세요')

        elif want == '2':
            check_booked()

        elif want == '3':
            delete_booked()

        elif want == 'home':
            print('홈 화면으로 돌아갑니다\n')
            break
        else:
            print('다시 입력해주세요')


if __name__ == '__main__':
    print("********** 눈송 시네마에 오신 걸 환영합니다 **********")
    cursor = conn.cursor()

    while True:
        user_id, user_pw = login()

        cursor.execute("Select * from MEMBER where (MEMBER.ID=(%s))", user_id)
        row = cursor.fetchone()
        if row[1].strip() == user_id and row[2].strip() == user_pw:
            print(f"안녕하세요 {row[0].strip()}님")
            while True:
                print("========== 메뉴 선택 ==========\n"
                      "1. 현재 상영 중인 영화 확인\n"
                      "2. 영화 예매\n"
                      "3. 마이 페이지\n"
                      "4. 종료\n"
                      "==============================")
                menu = input("원하시는 메뉴를 숫자로 입력해주세요: ")

                if menu == '1':
                    currently_showing()
                elif menu == '2':
                    buy_ticket()
                elif menu == '3':
                    my_page()
                elif menu == '4':
                    print("\n**********************************\n"
                          "  눈송시네마를 이용해주셔서 감사합니다. \n"
                          "**********************************\n")
                    quit()
                else:
                    print('다시 입력해주세요')
        else:
            print("로그인에 실패하셨습니다. 아이디와 비밀번호를 다시 입력해주세요")
