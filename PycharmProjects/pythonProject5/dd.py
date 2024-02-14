class Movie:
    def __init__(self, name, genre, duration):
        self.name = name
        self.genre = genre
        self.duration = duration

    def movieInfo(self):
        return f"Movie Name:{self.name}\nMovie Genre:{self.genre}\nMovie Duration:{self.duration} minutes."

    @classmethod
    def createMovie_fromString(cls, movie_string):
        name, genre, duration = movie_string.split('-')
        duration = int(duration)
        return cls(name, genre, duration)


class StarCinema:
    all_branch_info = {}

    def __init__(self, branch_name):
        self.branch_name = branch_name
        self.movie_list = []
        StarCinema.all_branch_info[self.branch_name] = self.movie_list
        print(f'Welcome to the {self.branch_name} branch of StarCinema!')

    def addMovies(self, *movie_objects):
        for movie in movie_objects:
            if movie not in self.movie_list:
                self.movie_list.append(movie)
                StarCinema.all_branch_info[self.branch_name] = self.movie_list
                print(f"{movie.name} added to {self.branch_name} branch.")
            else:
                print("Movie is already added in this branch.")

    def removeMovie(self, movie_object):
        if movie_object in self.movie_list:
            self.movie_list.remove(movie_object)
            StarCinema.all_branch_info[self.branch_name] = self.movie_list

    @classmethod
    def check(cls, movie_name):
        b_list = []
        st_list = []
        for b_n, movie_list in cls.all_branch_info.items():
            for movie in movie_list:
                if movie.name == movie_name:
                    b_list.append(b_n)
                    st_list.append(movie.genre)
                    st_list.append(movie.duration)
                    break

        if st_list:
            for i in b_list:
                print(f"{movie_name} is being streamed in {i} branch.")
            print(f"It is of {st_list[0]} genre and {st_list[1]} minutes duration.")
        else:
            print(f"{movie_name} is not being streamed in any branch.")

    @classmethod
    def showAllBranchInfo(cls):
        for b_n, movie_list in cls.all_branch_info.items():
            print(f"Branch Name:{b_n}")
            for j, m in enumerate(movie_list, start=1):
                print(f"Movie No: {j}\n{m.movieInfo()}\n**************************")
            print("#################################")


# Driver code
movie1 = Movie('Oppenheimer', 'Biographical Drama', 180)
movie2 = Movie('Barbie', 'Fantasy Comedy', 114)
movie3 = Movie('Mission: Impossible – Dead Reckoning Part One', 'Action', 163)
print('1==========================================')
print(movie3.movieInfo())
print('2==========================================')
movie4 = Movie.createMovie_fromString('Prohelika-Drama-153')
print('3==========================================')
print(movie4.movieInfo())
print('4==========================================')
branch1 = StarCinema('Mohakhali')
print('5==========================================')
branch1.addMovies(movie1, movie2, movie4)
print('6==========================================')
branch1.addMovies(movie1, movie3)
print('7==========================================')
StarCinema.showAllBranchInfo()
print('8==========================================')
branch2 = StarCinema('Mirpur')
print('9==========================================')
branch2.addMovies(movie1, movie2, movie3)
print('10=========================================')
StarCinema.showAllBranchInfo()
print('11=========================================')
StarCinema.check('Oppenheimer')
print('12=========================================')
StarCinema.check('Sound of Freedom')
print('13=========================================')
branch1.removeMovie(movie2)
StarCinema.showAllBranchInfo()
print('14=========================================')
branch2.removeMovie(movie1)
StarCinema.showAllBranchInfo()
