import flet as ft
from flet import KeyboardEvent
from expression import Expression
from calculate import Calculate
from addspaces import add_spaces


symbols = [",", "(", ")", ".", "-", "+", "÷", "×", "=", "C"]


def main(page: ft.Page):
    # Build expression as string
    expression = Expression()
    # Evaluate expression
    calculate = Calculate()

    page.title = "Flet Calculator by M.Artyszewicz"
    page.window_width = 300
    page.window_height = 460
    page.bgcolor = "#000000"

    value = ""
    global data
    data = "0"

    # Functions handling buttons and keyboard
    def on_click(e):
        data = e.control.data
        calculator(data)
        return data

    def on_keyboard(e: KeyboardEvent) -> str:
        data = e.key
        shift = e.shift
        key_mapping = {"=": "+", "8": "×", "9": "( )", "0": "( )"}
        if shift and data in key_mapping:
            data = key_mapping[data]
            calculator(data)
        else:
            if data.isdigit():
                calculator(data)
                return data
            elif data in symbols:
                calculator(data)
                return data
            elif data == "Enter":
                calculator("=")
            elif data == "Backspace":
                calculator("<")
            elif data == "/":
                calculator("÷")

    # main function
    def calculator(data):
        result = expression.handle_button_click(data)
        result = add_spaces(result)
        print(result)
        user_input.value = result

        try:
            evaluate_expression = calculate.evaluate_expression(result)
            if evaluate_expression == "ZeroDivision":
                result_area.value = "Error: division by zero"
            else:
                result_area.value = add_spaces(evaluate_expression)

            if evaluate_expression == 0.0:
                result_area.value = "0"

            if data == "=":
                user_input.value = str(evaluate_expression).replace('.', ',')
                str_result = str(evaluate_expression).replace('.', ',')
                result = expression.handle_button_click("C")
                for x in str_result:
                    result = expression.handle_button_click("+/-" if x == "-" else x)
                result_area.value = ""
        except:
            result_area.value = ""

        page.update()
        return value

    # Create user input area and result area
    user_input = ft.TextField(
        read_only=True,
        text_style=ft.TextStyle(size=30, color="#FBFBFB"),
        text_align=ft.TextAlign.RIGHT,
        multiline=True,
        min_lines=2,
        expand=True,
    )

    result_area = ft.TextField(
        read_only=True,
        text_style=ft.TextStyle(size=20, color="#333333"),
        text_align=ft.TextAlign.RIGHT,
        height=60,
        min_lines=1,
    )

    page.add(user_input, result_area)

    # Create buttons
    class Button(ft.ElevatedButton):
        def __init__(self, text, bgcolor, color, data, on_click):
            super().__init__(
                text=text,
                bgcolor=bgcolor,
                color=color,
                style=ft.ButtonStyle(padding=0),
                on_click=on_click
            )
            self.data = data

    btn_clear = Button("C", "#A5A5A5", "#000000", "C", on_click)
    btn_back = Button("<", "#A5A5A5", "#000000", "<", on_click)
    btn_bracket = Button("( )", "#A5A5A5", "#000000", "( )", on_click)
    btn_divide = Button("÷", "#CA3302", "#FBFBFB", "÷", on_click)
    row1 = ft.Row(
        controls=[btn_clear, btn_back, btn_bracket, btn_divide],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    btn_7 = Button("7", "#333333", "#FBFBFB", "7", on_click)
    btn_8 = Button("8", "#333333", "#FBFBFB", "8", on_click)
    btn_9 = Button("9", "#333333", "#FBFBFB", "9", on_click)
    btn_mult = Button("×", "#CA3302", "#FBFBFB", "×", on_click)
    row2 = ft.Row(
        controls=[btn_7, btn_8, btn_9, btn_mult],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    btn_4 = Button("4", "#333333", "#FBFBFB", "4", on_click)
    btn_5 = Button("5", "#333333", "#FBFBFB", "5", on_click)
    btn_6 = Button("6", "#333333", "#FBFBFB", "6", on_click)
    btn_subt = Button("-", "#CA3302", "#FBFBFB", "-", on_click)
    row3 = ft.Row(
        controls=[btn_4, btn_5, btn_6, btn_subt],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    btn_1 = Button("1", "#333333", "#FBFBFB", "1", on_click)
    btn_2 = Button("2", "#333333", "#FBFBFB", "2", on_click)
    btn_3 = Button("3", "#333333", "#FBFBFB", "3", on_click)
    btn_add = Button("+", "#CA3302", "#FBFBFB", "+", on_click)
    row4 = ft.Row(
        controls=[btn_1, btn_2, btn_3, btn_add],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    btn_neg = Button("+/-", "#333333", "#FBFBFB", "+/-", on_click)
    btn_0 = Button("0", "#333333", "#FBFBFB", "0", on_click)
    btn_dot = Button(",", "#333333", "#FBFBFB", ",", on_click)
    btn_res = Button("=", "#CA3302", "#FBFBFB", "=", on_click)
    row5 = ft.Row(
        controls=[btn_neg, btn_0, btn_dot, btn_res],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    rows = [row1, row2, row3, row4, row5]

    for row in rows:
        page.add(row)

    page.on_keyboard_event = on_keyboard
    page.update()


ft.app(target=main)
