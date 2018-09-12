import os


class Data:
    data = []
    cur_user = None
    cur_year = None
    cur_month = None
    cur_day = None


class Diary(Data):
    def __init__(self, user_name):
        self.cur_user = user_name
        self.update_data()

    def update_data(self):
        files = [file for file in os.listdir("users/" + self.cur_user)
                 if os.path.isfile('/'.join(["users", self.cur_user, file]))]
        self.data = [list(map(int, line.split('_'))) for line in files]

    def change_user(self, user_name):
        self.cur_user = user_name
        self.update_data()
        self.cur_year, self.cur_month, self.cur_day = [None, None, None]

    def set_cur_year(self, year):
        self.cur_year = year

    def set_cur_month(self, month):
        self.cur_month = month

    def set_cur_day(self, day):
        self.cur_day = day

    def get_year(self):
        year_list = [date[0] for date in self.data]
        return list(set(year_list))

    def get_month(self, year=None):
        if year is not None:
            self.cur_year = year
        month_list = [date[1] for date in self.data if date[0] == self.cur_year]
        return sorted(list(set(month_list)))

    def get_day(self, month=None, year=None):
        if month is not None:
            self.cur_month = month
        if year is not None:
            self.cur_year = year
        day_list = [date[2] for date in self.data
                    if date[0] == self.cur_year and date[1] == self.cur_month]
        return sorted(day_list)

    def get_cur_user(self):
        return self.cur_user

    def load_diary(self, year=None, month=None, day=None):
        if year is not None:
            self.cur_year = year
        if month is not None:
            self.cur_month = month
        if day is not None:
            self.cur_day = day
        path = self.get_cur_path()
        with open(path, 'r') as cur_diary:
            text = cur_diary.read()

        return text

    def save_diary(self, new_diary):
        path = self.get_cur_path()
        with open(path, 'r+') as cur_diary:
            cur_diary.truncate()
            cur_diary.write(new_diary)

    def create_diary(self):
        path = self.get_cur_path()
        new_diary = open(path, 'w')
        new_diary.close()

    def get_cur_path(self):
        str_cur_year = str(self.cur_year)
        str_cur_month = "0" + str(self.cur_month) if self.cur_month < 10 else str(self.cur_month)
        str_cur_day = "0" + str(self.cur_day) if self.cur_day < 10 else str(self.cur_day)
        file = '_'.join([str_cur_year, str_cur_month, str_cur_day])
        path = '/'.join(["users", self.cur_user, file])
        return path


def get_user():
    user_list = [name for name in os.listdir("users/") if os.path.isdir("users/" + name)]
    return user_list
