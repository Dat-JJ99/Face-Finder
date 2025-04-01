from guizero import App, Text, PushButton, Picture

app = App(title="guizero", bg = "black", height = 1080, width = 1920)

logo = Picture(app, image='logo.PNG', align="left", align="top" , width= 100, height= 1000)


app.display()