import time
import flet as ft
from flet import KeyboardEvent
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
LIGHT_TEXT = "#FBFBFB"
DARK_TEXT = "#000000"
LIGHT_MODE_COLORS = {
    "TOP_BUTTONS":"#3ecace",
    "RIGHT_BUTTONS":"#24948c",
    "BOTTOM_BUTTONS":"#9ff0ea",
}
DARK_MODE_COLORS = {
    "TOP_BUTTONS":"#A5A5A5",
    "RIGHT_BUTTONS":"#CA3302",
    "BOTTOM_BUTTONS":"#333333",
}

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
        time.sleep(0.3)
        for row in rows_light:
            row.visible = True if page.theme_mode == "light" else False
        for row in rows_dark:
            row.visible = True if page.theme_mode == "dark" else False
        switch.label = ("Light mode" if page.theme_mode == "light" else "Dark mode")
        page.update()

    switch = ft.Switch(
        label="Light mode",
        on_change=changetheme,
        inactive_thumb_color=LIGHT_MODE_COLORS["RIGHT_BUTTONS"],
        inactive_track_color=LIGHT_MODE_COLORS["BOTTOM_BUTTONS"],
        active_color=DARK_MODE_COLORS["RIGHT_BUTTONS"],
        active_track_color=DARK_MODE_COLORS["BOTTOM_BUTTONS"]
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

    page.add(switch, user_input, result_area)

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

    btn_clear_dark = Button("C", DARK_MODE_COLORS["TOP_BUTTONS"], DARK_TEXT, "C", on_click)
    btn_back_dark = Button("<", DARK_MODE_COLORS["TOP_BUTTONS"], DARK_TEXT, "<", on_click)
    btn_bracket_dark = Button("( )", DARK_MODE_COLORS["TOP_BUTTONS"], DARK_TEXT, "( )", on_click)
    btn_divide_dark = Button("÷", DARK_MODE_COLORS["RIGHT_BUTTONS"], LIGHT_TEXT, "÷", on_click)
    row1_dark = ft.Row(
        controls=[btn_clear_dark, btn_back_dark, btn_bracket_dark, btn_divide_dark],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=False,
    )
    btn_clear_light = Button("C", LIGHT_MODE_COLORS["TOP_BUTTONS"], LIGHT_TEXT, "C", on_click)
    btn_back_light = Button("<", LIGHT_MODE_COLORS["TOP_BUTTONS"], LIGHT_TEXT, "<", on_click)
    btn_bracket_light = Button("( )", LIGHT_MODE_COLORS["TOP_BUTTONS"], LIGHT_TEXT, "( )", on_click)
    btn_divide_light = Button("÷", LIGHT_MODE_COLORS["RIGHT_BUTTONS"], LIGHT_TEXT, "÷", on_click)
    row1_light = ft.Row(
        controls=[btn_clear_light, btn_back_light, btn_bracket_light, btn_divide_light],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=True,
    )

    btn_7_dark = Button("7", DARK_MODE_COLORS["BOTTOM_BUTTONS"], LIGHT_TEXT, "7", on_click)
    btn_8_dark = Button("8", DARK_MODE_COLORS["BOTTOM_BUTTONS"], LIGHT_TEXT, "8", on_click)
    btn_9_dark = Button("9", DARK_MODE_COLORS["BOTTOM_BUTTONS"], LIGHT_TEXT, "9", on_click)
    btn_mult_dark = Button("×", DARK_MODE_COLORS["RIGHT_BUTTONS"], LIGHT_TEXT, "×", on_click)
    row2_dark = ft.Row(
        controls=[btn_7_dark, btn_8_dark, btn_9_dark, btn_mult_dark],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=False,
    )
    btn_7_light = Button("7", LIGHT_MODE_COLORS["BOTTOM_BUTTONS"], DARK_TEXT, "7", on_click)
    btn_8_light = Button("8", LIGHT_MODE_COLORS["BOTTOM_BUTTONS"], DARK_TEXT, "8", on_click)
    btn_9_light = Button("9", LIGHT_MODE_COLORS["BOTTOM_BUTTONS"], DARK_TEXT, "9", on_click)
    btn_mult_light = Button("×", LIGHT_MODE_COLORS["RIGHT_BUTTONS"], LIGHT_TEXT, "×", on_click)
    row2_light = ft.Row(
        controls=[btn_7_light, btn_8_light, btn_9_light, btn_mult_light],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=True,
    )

    btn_4_dark = Button("4", DARK_MODE_COLORS["BOTTOM_BUTTONS"], LIGHT_TEXT, "4", on_click)
    btn_5_dark = Button("5", DARK_MODE_COLORS["BOTTOM_BUTTONS"], LIGHT_TEXT, "5", on_click)
    btn_6_dark = Button("6", DARK_MODE_COLORS["BOTTOM_BUTTONS"], LIGHT_TEXT, "6", on_click)
    btn_subt_dark = Button("-", "#CA3302", LIGHT_TEXT, "-", on_click)
    row3_dark = ft.Row(
        controls=[btn_4_dark, btn_5_dark, btn_6_dark, btn_subt_dark],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=False,
    )
    btn_4_light = Button("4", LIGHT_MODE_COLORS["BOTTOM_BUTTONS"], DARK_TEXT, "4", on_click)
    btn_5_light = Button("5", LIGHT_MODE_COLORS["BOTTOM_BUTTONS"], DARK_TEXT, "5", on_click)
    btn_6_light = Button("6", LIGHT_MODE_COLORS["BOTTOM_BUTTONS"], DARK_TEXT, "6", on_click)
    btn_subt_light = Button("-", LIGHT_MODE_COLORS["RIGHT_BUTTONS"], LIGHT_TEXT, "-", on_click)
    row3_light = ft.Row(
        controls=[btn_4_light, btn_5_light, btn_6_light, btn_subt_light],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=True,
    )

    btn_1_dark = Button("1", DARK_MODE_COLORS["BOTTOM_BUTTONS"], LIGHT_TEXT, "1", on_click)
    btn_2_dark = Button("2", DARK_MODE_COLORS["BOTTOM_BUTTONS"], LIGHT_TEXT, "2", on_click)
    btn_3_dark = Button("3", DARK_MODE_COLORS["BOTTOM_BUTTONS"], LIGHT_TEXT, "3", on_click)
    btn_add_dark = Button("+", DARK_MODE_COLORS["RIGHT_BUTTONS"], LIGHT_TEXT, "+", on_click)
    row4_dark = ft.Row(
        controls=[btn_1_dark, btn_2_dark, btn_3_dark, btn_add_dark],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=False,
    )
    btn_1_light = Button("1", LIGHT_MODE_COLORS["BOTTOM_BUTTONS"], DARK_TEXT, "1", on_click)
    btn_2_light = Button("2", LIGHT_MODE_COLORS["BOTTOM_BUTTONS"], DARK_TEXT, "2", on_click)
    btn_3_light = Button("3", LIGHT_MODE_COLORS["BOTTOM_BUTTONS"], DARK_TEXT, "3", on_click)
    btn_add_light = Button("+", LIGHT_MODE_COLORS["RIGHT_BUTTONS"], LIGHT_TEXT, "+", on_click)
    row4_light = ft.Row(
        controls=[btn_1_light, btn_2_light, btn_3_light, btn_add_light],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=True,
    )

    btn_neg_dark = Button("+/-", DARK_MODE_COLORS["BOTTOM_BUTTONS"], LIGHT_TEXT, "+/-", on_click)
    btn_0_dark = Button("0", DARK_MODE_COLORS["BOTTOM_BUTTONS"], LIGHT_TEXT, "0", on_click)
    btn_dot_dark = Button(",", DARK_MODE_COLORS["BOTTOM_BUTTONS"], LIGHT_TEXT, ",", on_click)
    btn_res_dark = Button("=", DARK_MODE_COLORS["RIGHT_BUTTONS"], LIGHT_TEXT, "=", on_click)
    row5_dark = ft.Row(
        controls=[btn_neg_dark, btn_0_dark, btn_dot_dark, btn_res_dark],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        visible=False,
    )
    btn_neg_light = Button("+/-", LIGHT_MODE_COLORS["BOTTOM_BUTTONS"], DARK_TEXT, "+/-", on_click)
    btn_0_light = Button("0", LIGHT_MODE_COLORS["BOTTOM_BUTTONS"], DARK_TEXT, "0", on_click)
    btn_dot_light = Button(",", LIGHT_MODE_COLORS["BOTTOM_BUTTONS"], DARK_TEXT, ",", on_click)
    btn_res_light = Button("=", LIGHT_MODE_COLORS["RIGHT_BUTTONS"], LIGHT_TEXT, "=", on_click)
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
