from colorama import init, Fore,Back,Style
from tabulate import tabulate



class Styles:
    def __init__(self):
        self._list_format = "simple"

        self._background = Back.RESET
        self._font_color = Fore.WHITE
        self._font_style = Style.NORMAL
        self._style_menu = None

    def demo_show(self, format):
        demo_show = [["Demo First Name", "Demo Last Name", "Demo Email"]]
        return tabulate(demo_show, headers=["Header Name", "Header Last Name", "Header Email"], tablefmt = format)

    def font_style_menu(self):
            while True:
                self.new_print( Style.BRIGHT + "1. Bright font")
                self.new_print( Style.DIM + "2. Dim font")
                self.new_print( Style.NORMAL + "3. Normal font")
                self.new_print( Style.RESET_ALL + "4. Reset all font style settings")
                self.new_print("5. Return")
                choice = input("Enter your choice: ")
                if choice == "1":
                    self._font_style = Style.BRIGHT
                elif choice == "2":
                    self._font_style = Style.DIM
                elif choice == "3":
                    self._font_style = Style.NORMAL
                elif choice == "4":
                    self._font_style = Style.RESET_ALL
                elif choice == "5":
                    return self._font_style
                else:
                    self.new_print("Invalid input")
    
    def font_color_menu(self):
        while True:
            self.new_print( Fore.BLACK + "1. Black font")
            self.new_print( Fore.RED + "2. Red font")
            self.new_print( Fore.GREEN + "3. Green font")
            self.new_print( Fore.YELLOW + "4. Yellow font")
            self.new_print( Fore.BLUE + "5. Blue font")
            self.new_print( Fore.MAGENTA + "6. Magenta font")
            self.new_print( Fore.CYAN + "7. Cyan font")
            self.new_print( Fore.WHITE + "8. White font")
            self.new_print("9. Return")
            choice = input("Enter a number of color to change: ")
            if choice == "1":
                self._font_color = Fore.BLACK
            elif choice == "2":
                self._font_color = Fore.RED
            elif choice == "3":
                self._font_color = Fore.GREEN
            elif choice == "4":
                self._font_color = Fore.YELLOW
            elif choice == "5":
                self._font_color = Fore.BLUE
            elif choice == "6":
                self._font_color = Fore.MAGENTA
            elif choice == "7":
                self._font_color = Fore.CYAN
            elif choice == "8":
                self._font_color = Fore.WHITE
            elif choice == "9":
                return self._font_color
            else:
                self.new_print("Invalid input")

    def background_menu(self):
        while True:
            self.new_print(Back.BLACK + "1. Black background")
            self.new_print(Back.RED + "2. Red background")
            self.new_print(Back.GREEN + "3. Green background")
            self.new_print(Back.YELLOW + "4. Yellow background")
            self.new_print(Back.BLUE + "5. Blue background")
            self.new_print(Back.MAGENTA + "6. Magenta background")
            self.new_print(Back.CYAN + "7. Cyan background")
            self.new_print(Back.WHITE + "8. White background")
            self.new_print("9. Return to previus menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                self._background = Back.BLACK
            elif choice == "2":
                self._background = Back.RED
            elif choice == "3":
                self._background = Back.GREEN
            elif choice == "4":
                self._background = Back.YELLOW
            elif choice == "5":
                self._background = Back.BLUE
            elif choice == "6":
                self._background = Back.MAGENTA
            elif choice == "7":
                self._background = Back.CYAN
            elif choice == "8":
                self._background = Back.WHITE
            elif choice == "9":
                return self._background
            else:
                self.new_print("Invalid input")
        
    def list_style_menu(self):
        while True:
            self.new_print("1. Plain")
            self.new_print("2. Simple")
            self.new_print("3. Grid")
            self.new_print("4. Youtrack")
            self.new_print("5. Orgtbl")
            self.new_print("6. Rst")
            self.new_print("7. Mediawiki")
            self.new_print("8. Html")
            self.new_print("9. Pretty")
            self.new_print("10. Return to previus menu")
            format_choice = input("Enter a number of the format to try or\nEnter the name of format to change: ").lower()
            if format_choice == "1":
                self.new_print(self.demo_show("plain"))
            elif format_choice == "2":
                self.new_print(self.demo_show("simple"))
            elif format_choice == "3":
                self.new_print(self.demo_show("grid"))
            elif format_choice == "4":
                self.new_print(self.demo_show("youtrack"))
            elif format_choice == "5":
                self.new_print(self.demo_show("orgtbl"))
            elif format_choice == "6":
                self.new_print(self.demo_show("rst"))
            elif format_choice == "7":
                self.new_print(self.demo_show("mediawiki"))
            elif format_choice == "8":
                self.new_print(self.demo_show("html"))
            elif format_choice == "9":
                self.new_print(self.demo_show("pretty"))
            elif format_choice == "10":
                return
            elif format_choice in ["plain", "simple", "grid", "youtrack", "orgtbl", "rst", "mediawiki", "html", "pretty"]:
                self._list_format = format_choice
                return self._list_format
            else:
                self.new_print("Invalid input.")

    def style_settings_menu(self):
        while True:
            self.new_print("1. Font color menu ")
            self.new_print("2. Font style menu ")
            self.new_print("3. Background menu")
            self.new_print("4. List style menu")
            self.new_print("5. Reset all styles")
            self.new_print("6. Return to main menu")

            choice = input("Enter your choice: ")
            if choice == "1":
                self.font_color_menu()
            elif choice == "2":
                self.font_style_menu()
            elif choice == "3":
                self.background_menu()
            elif choice == "4":
                self.list_style_menu()
            elif choice == "5":
                self._font_style = Style.NORMAL
                self._font_color = Fore.WHITE
                self._background = Back.RESET
                self.list_format = "plain"
            elif choice == "6":
                return 
            else:
                self.new_print("Invalid input")

    
    def background(self):
        return self._background
    def font_color(self):
        return self._font_color
    def font_style(self):
        return self._font_style
    def list_format(self):
        return self._list_format
    def new_print(self, text = None):
        return print(self._font_color + self._background + self._font_style + f"{text}")

if __name__ == "__main__":
    style = Styles()
    style.style_settings_menu()