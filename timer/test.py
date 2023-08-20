import pathlib
import time
import PySimpleGUI as sg

sg.theme('default1')
path = pathlib.Path('user_set.txt')

timer_count = 5

def set_time(timer_index):
    layout = [
        [sg.Text(f'タイマー {timer_index + 1} をセットします')],
        [sg.Spin([m for m in range(61)], size=2, font=(None, 15)), sg.T('分'),
         sg.Spin([s for s in range(60)], size=2, font=(None, 15)), sg.T('秒')],
        [sg.Checkbox('デフォルトとして設定する', key='-DEFAULT-')],
        [sg.OK(), sg.Cancel()]
    ]

    window = sg.Window(f'セットタイマー {timer_index + 1}', layout, size=(250, 160), element_justification='center')

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        user = (0, 0)
    elif event == 'OK':
        user = (values[0], values[1])
        if values['-DEFAULT-']:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f'{values[0]} {values[1]}')
    window.close()
    return user

def main():
    started = [False] * timer_count
    if path.exists():
        with open(path, encoding='utf-8') as f:
            user_min, user_sec = map(int, f.read().split())
    else:
        user_min, user_sec = (0, 0)

    current_min = [user_min] * timer_count
    current_sec = [user_sec] * timer_count
    end_time = [time.time()] * timer_count
    completed = [False] * timer_count

    button_active_color = ('black', 'green')
    button_default_color = ('black', 'red')

    layout = [
        [sg.Text('イライラ解決タイマー', font=(None, 15))],
    ]

    for timer_index in range(timer_count):
        layout.append([sg.Text(f'NO.{timer_index + 1}:',font=('Gothic',13,'bold')),
                       sg.Text('', font=(None, 30), pad=(0, 0), key=f'-DISPLAY-{timer_index}-')])
        layout.append([
            sg.B('オリジナル', key=f'-PRESET-OR-{timer_index}-', size=(15, 3), button_color=button_default_color, font=('Gothic', 13, 'bold')),
            sg.B('レッド', key=f'-PRESET-RH-{timer_index}-', size=(15, 3), button_color=button_default_color, font=('Gothic', 13, 'bold')),
            sg.B('フィレ', key=f'-PRESET-F-{timer_index}-', size=(15, 3), button_color=button_default_color, font=('Gothic', 13, 'bold')),
        ])
        layout.append([
            sg.B('リセット', key=f'-RESET-{timer_index}-', size=(15, 3), button_color=button_default_color, font=('Gothic', 13, 'bold')),
        ])

    window = sg.Window('タイマー', layout, size=(1920, 1080), element_justification='center', resizable=True, finalize=True)

    def update_display(timer_index):
        if started[timer_index]:
            if completed[timer_index]:
                window[f'-DISPLAY-{timer_index}-'].update(f'調理完了')
            elif current_min[timer_index] >= 5:
                window[f'-DISPLAY-{timer_index}-'].update(f'調理中［{int(current_min[timer_index])} : {int(current_sec[timer_index])}］')
            else:
                window[f'-DISPLAY-{timer_index}-'].update(f'ボーンダウン中［{int(current_min[timer_index])} : {int(current_sec[timer_index])}］')
        else:
            window[f'-DISPLAY-{timer_index}-'].update('')

    while True:
        event, values = window.read(timeout=50)
        if event == sg.WIN_CLOSED or event == 'Quit':
            break

        for timer_index in range(timer_count):
            if event == f'-STOP-{timer_index}-':
                started[timer_index] = False
                completed[timer_index] = False
            elif event == f'-RESET-{timer_index}-':
                started[timer_index] = False
                completed[timer_index] = False
                current_min[timer_index], current_sec[timer_index] = user_min, user_sec
                update_display(timer_index)
                window[f'-PRESET-OR-{timer_index}-'].update(button_color=button_default_color)
                window[f'-PRESET-RH-{timer_index}-'].update(button_color=button_default_color)
                window[f'-PRESET-F-{timer_index}-'].update(button_color=button_default_color)
            elif event.startswith(f'-PRESET-'):
                preset_timers = {f'-PRESET-OR-{timer_index}-': 20, f'-PRESET-RH-{timer_index}-': 5.1, f'-PRESET-F-{timer_index}-': 0.10}
                preset_time = preset_timers.get(event)
                if preset_time is not None:
                    user_min, user_sec = preset_time, 0
                    current_min[timer_index], current_sec[timer_index] = user_min, user_sec
                    update_display(timer_index)
                    started[timer_index] = True
                    completed[timer_index] = False
                    end_time[timer_index] = time.time() + current_min[timer_index] * 60 + current_sec[timer_index]
                    button_key = event.split('-')[2]
                    window[event].update(button_color=button_active_color)
                    window[f'-DISPLAY-{timer_index}-'].update(f'ボタン: {event}')

            if started[timer_index]:
                remaining_time = end_time[timer_index] - time.time()
                if remaining_time > 0:
                    current_min[timer_index], current_sec[timer_index] = divmod(remaining_time, 60)
                else:
                    if not completed[timer_index]:
                        completed[timer_index] = True
                    current_min[timer_index], current_sec[timer_index] = 0, 0
                update_display(timer_index)

    window.close()

if __name__ == '__main__':
    main()
