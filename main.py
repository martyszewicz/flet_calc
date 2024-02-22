import time

import flet as ft
from flet import KeyboardEvent
from flet_core import IconButton, ButtonStyle, colors

from expression import Expression
from calculate import Calculate
from addspaces import add_spaces

BUTTON_TEXT_SIZE = 25
BUTTON_WIDTH = 85
BUTTON_HEIGHT = 50
WINDOW_WIDTH = 412
WINDOW_HEIGHT = 732
RESULT_AREA_HEIGHT = 100
RESULT_AREA_TEXT_SIZE = 35
USER_INPUT_TEXT_SIZE = 50

symbols = [",", "(", ")", ".", "-", "+", "÷", "×", "=", "C"]


def main(page: ft.Page):
    page.theme_mode = "light"
    page.add(
        ft.SafeArea(
            content=ft.Text("Calculator created by M. Artyszewicz", size=10)
        ),
    )

    def changetheme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        time.sleep(0.5)
        toogledarklight.selected = not toogledarklight.selected
        for row in rows_light:
            row.visible = True if page.theme_mode == "light" else False
        for row in rows_dark:
            row.visible = True if page.theme_mode == "dark" else False
        print(page.theme_mode)
        page.update()

    toogledarklight = IconButton(
        on_click=changetheme,
        icon="dark_mode",
        selected_icon="light_mode",
        style=ButtonStyle(
            color={"": colors.BLACK, "selected": colors.WHITE}
        )
    )

    # Build expression as string
    expression = Expression()
    # Evaluate expression
    calculate = Calculate()

    page.title = "Flet Calculator by M.Artyszewicz"
    page.window_width = WINDOW_WIDTH
    page.window_height = WINDOW_HEIGHT

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
                user_input.value = str(add_spaces(evaluate_expression)).replace('.', ',')
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
        text_style=ft.TextStyle(size=USER_INPUT_TEXT_SIZE),
        text_align=ft.TextAlign.RIGHT,
        multiline=True,
        min_lines=2,
        expand=True,
    )

    result_area = ft.TextField(
        read_only=True,
        text_style=ft.TextStyle(size=RESULT_AREA_TEXT_SIZE),
        text_align=ft.TextAlign.RIGHT,
        height=RESULT_AREA_HEIGHT,
        min_lines=1,
    )

    page.add(toogledarklight, user_input, result_area)

    # Create buttons
    class Button(ft.ElevatedButton):
        def __init__(self, text, bgcolor, color, data, on_click):
            super().__init__(
                bgcolor=bgcolor,
                color=color,
                style=ft.ButtonStyle(padding=0),
                on_click=on_click,
            )
            self.text = text
            self.content = ft.Column(
                [ft.Text(value=self.text, size=BUTTON_TEXT_SIZE)],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            self.data = data
            self.width = BUTTON_WIDTH
            self.height = BUTTON_HEIGHT

    btn_clear_dark = Button("C", "#A5A5A5", "#000000", "C", on_click)
    btn_back_dark = Button("<", "#A5A5A5", "#000000", "<", on_click)
    btn_bracket_dark = Button("( )", "#A5A5A5", "#000000", "( )", on_click)
    btn_divide_dark = Button("÷", "#CA3302", "#FBFBFB", "÷", on_click)
    row1_dark = ft.Row(
        controls=[btn_clear_dark, btn_back_dark, btn_bracket_dark, btn_divide_dark],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=False,
    )
    btn_clear_light = Button("C", "#3ecace", "#FBFBFB", "C", on_click)
    btn_back_light = Button("<", "#3ecace", "#FBFBFB", "<", on_click)
    btn_bracket_light = Button("( )", "#3ecace", "#FBFBFB", "( )", on_click)
    btn_divide_light = Button("÷", "#24948c", "#FBFBFB", "÷", on_click)
    row1_light = ft.Row(
        controls=[btn_clear_light, btn_back_light, btn_bracket_light, btn_divide_light],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=True,
    )

    btn_7_dark = Button("7", "#333333", "#FBFBFB", "7", on_click)
    btn_8_dark = Button("8", "#333333", "#FBFBFB", "8", on_click)
    btn_9_dark = Button("9", "#333333", "#FBFBFB", "9", on_click)
    btn_mult_dark = Button("×", "#CA3302", "#FBFBFB", "×", on_click)
    row2_dark = ft.Row(
        controls=[btn_7_dark, btn_8_dark, btn_9_dark, btn_mult_dark],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=False,
    )
    btn_7_light = Button("7", "#9ff0ea", "#000000", "7", on_click)
    btn_8_light = Button("8", "#9ff0ea", "#000000", "8", on_click)
    btn_9_light = Button("9", "#9ff0ea", "#000000", "9", on_click)
    btn_mult_light = Button("×", "#24948c", "#FBFBFB", "×", on_click)
    row2_light = ft.Row(
        controls=[btn_7_light, btn_8_light, btn_9_light, btn_mult_light],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=True,
    )

    btn_4_dark = Button("4", "#333333", "#FBFBFB", "4", on_click)
    btn_5_dark = Button("5", "#333333", "#FBFBFB", "5", on_click)
    btn_6_dark = Button("6", "#333333", "#FBFBFB", "6", on_click)
    btn_subt_dark = Button("-", "#CA3302", "#FBFBFB", "-", on_click)
    row3_dark = ft.Row(
        controls=[btn_4_dark, btn_5_dark, btn_6_dark, btn_subt_dark],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=False,
    )
    btn_4_light = Button("4", "#9ff0ea", "#000000", "4", on_click)
    btn_5_light = Button("5", "#9ff0ea", "#000000", "5", on_click)
    btn_6_light = Button("6", "#9ff0ea", "#000000", "6", on_click)
    btn_subt_light = Button("-", "#24948c", "#FBFBFB", "-", on_click)
    row3_light = ft.Row(
        controls=[btn_4_light, btn_5_light, btn_6_light, btn_subt_light],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=True,
    )

    btn_1_dark = Button("1", "#333333", "#FBFBFB", "1", on_click)
    btn_2_dark = Button("2", "#333333", "#FBFBFB", "2", on_click)
    btn_3_dark = Button("3", "#333333", "#FBFBFB", "3", on_click)
    btn_add_dark = Button("+", "#CA3302", "#FBFBFB", "+", on_click)
    row4_dark = ft.Row(
        controls=[btn_1_dark, btn_2_dark, btn_3_dark, btn_add_dark],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=False,
    )
    btn_1_light = Button("1", "#9ff0ea", "#000000", "1", on_click)
    btn_2_light = Button("2", "#9ff0ea", "#000000", "2", on_click)
    btn_3_light = Button("3", "#9ff0ea", "#000000", "3", on_click)
    btn_add_light = Button("+", "#24948c", "#FBFBFB", "+", on_click)
    row4_light = ft.Row(
        controls=[btn_1_light, btn_2_light, btn_3_light, btn_add_light],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=True,
    )

    btn_neg_dark = Button("+/-", "#333333", "#FBFBFB", "+/-", on_click)
    btn_0_dark = Button("0", "#333333", "#FBFBFB", "0", on_click)
    btn_dot_dark = Button(",", "#333333", "#FBFBFB", ",", on_click)
    btn_res_dark = Button("=", "#CA3302", "#FBFBFB", "=", on_click)
    row5_dark = ft.Row(
        controls=[btn_neg_dark, btn_0_dark, btn_dot_dark, btn_res_dark],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=False,
    )
    btn_neg_light = Button("+/-", "#9ff0ea", "#000000", "+/-", on_click)
    btn_0_light = Button("0", "#9ff0ea", "#000000", "0", on_click)
    btn_dot_light = Button(",", "#9ff0ea", "#000000", ",", on_click)
    btn_res_light = Button("=", "#24948c", "#FBFBFB", "=", on_click)
    row5_light = ft.Row(
        controls=[btn_neg_light, btn_0_light, btn_dot_light, btn_res_light],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=True,
    )

    rows_light = [row1_light, row2_light, row3_light, row4_light, row5_light]
    rows_dark = [row1_dark, row2_dark, row3_dark, row4_dark, row5_dark]

    for row in rows_light:
        page.add(row)
    for row in rows_dark:
        page.add(row)


    page.on_keyboard_event = on_keyboard
    page.update()


ft.app(main)
