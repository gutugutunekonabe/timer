from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

class TimerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')  # 背景色を白に変更
        self.timers = []

        for timer_number in range(1, 6):
            timer_layout = BoxLayout(orientation='horizontal')
            
            timer_number_label = Label(text=str(timer_number), font_size='24sp', bold=True)
            timer_label = Label(text="00:00", font_size='48sp')
            preset_button_layout = BoxLayout(orientation='vertical')

            timer_data = {
                "number_label": timer_number_label,
                "label": timer_label,
                "reset_button": None,
                "info_label": Label(text="", font_size='20sp'),
                "seconds": 0,
                "original_seconds": 0,
                "clock_event": None,
                "selected_preset": "",
                "preset_buttons": [],  # ボタンの状態を管理するリスト
            }

            for preset_text, seconds in [("Original", 20 * 60), ("RedHot", 5 * 65), ("Fillet", 5 * 5)]:
                preset_button = Button(text=preset_text, on_press=lambda instance, s=seconds, t=timer_data, p=preset_text: self.set_preset_timer(s, t, p))
                preset_button.bind(on_press=lambda instance: self.on_preset_button_press(instance, timer_data))  # ボタンが押されたときの処理をバインド
                preset_button_layout.add_widget(preset_button)
                timer_data["preset_buttons"].append(preset_button)  # リストに追加

            reset_button = Button(text="Reset", on_press=lambda instance, t=timer_data: self.reset_timer(t))
            timer_data["reset_button"] = reset_button

            timer_layout.add_widget(timer_number_label)
            timer_layout.add_widget(timer_label)
            timer_layout.add_widget(preset_button_layout)
            timer_layout.add_widget(reset_button)
            timer_layout.add_widget(timer_data["info_label"])

            self.timers.append(timer_data)

            self.layout.add_widget(timer_layout)
        
        self.selected_button = None  # 選択されたボタンを保持するプロパティ
        return self.layout
    
    def on_preset_button_press(self, instance, timer_data):
        # 選択されたボタンの色を戻す
        if self.selected_button:
            self.selected_button.background_color = (1, 1, 1, 1)
        
        # 押されたボタンの背景色を変更
        instance.background_color = (0, 1, 0, 1)  # 例: 緑色に変更
        self.selected_button = instance
    
    def reset_timer(self, timer_data):
        if timer_data["clock_event"]:
            self.stop_timer(timer_data)
            timer_data["seconds"] = timer_data["original_seconds"]
            self.update_time(timer_data)
            timer_data["label"].text = "00:00"
            timer_data["info_label"].text = ""
            
            # 全てのボタンの色をリセット
            for button in timer_data["preset_buttons"]:
                button.background_color = (1, 1, 1, 1)  # 白色に戻す
    
            if self.selected_button:
                self.selected_button.background_color = (1, 1, 1, 1)
                self.selected_button = None
    
            timer_data["selected_preset"] = ""

    def set_preset_timer(self, seconds, timer_data, preset_name):
        timer_data["seconds"] = seconds
        timer_data["original_seconds"] = seconds
        self.update_time(timer_data)
        self.start_timer(timer_data)
        timer_data["info_label"].text = f"{preset_name}, {seconds // 60} Min"
    
    def start_timer(self, timer_data):
        if timer_data["clock_event"] is None:
            timer_data["clock_event"] = Clock.schedule_interval(lambda dt: self.update_time(timer_data), 1)
    
    def reset_timer(self, timer_data):
        if timer_data["clock_event"]:
            self.stop_timer(timer_data)
            timer_data["seconds"] = timer_data["original_seconds"]
            self.update_time(timer_data)
            timer_data["label"].text = "00:00"
            timer_data["info_label"].text = ""
    
    def update_time(self, timer_data,dt=1):
        if timer_data["seconds"] > 0:
            timer_data["seconds"] -= 1
            minutes = timer_data["seconds"] // 60
            seconds = timer_data["seconds"] % 60
            timer_data["label"].text = f"{minutes:02}:{seconds:02}"

            # タイマーが5分以下になったら、"ボーンダウン中" と表示する
            if timer_data["seconds"] <= 300:
                timer_data["info_label"].text = "put on tray"
        else:
            self.stop_timer(timer_data)
            timer_data["label"].text = "00:00"
            timer_data["info_label"].text = "complete"
    
    def stop_timer(self, timer_data):
        if timer_data["clock_event"]:
            timer_data["clock_event"].cancel()
            timer_data["clock_event"] = None

if __name__ == '__main__':
    TimerApp().run()