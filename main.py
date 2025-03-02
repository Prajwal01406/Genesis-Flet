import flet as ft
import requests
import matplotlib.pyplot as plt
import uuid
import os

# App 
def main(pagee: ft.Page):
    pagee.title = 'Genesis'
    
# Home page variables

    # Container 1
    heading_cont_1 = ft.Container(
                                content= ft.Text("Multiple Programming Languages.",color='black',size=16,weight='bold',opacity=0.8,),
                                height=30,width=335,
                                border_radius=5,
                                alignment= ft.alignment.center,
                                bgcolor="#FFDAB3",
                            )
    
    text_cont_1  =   ft.Container(
                                content= ft.Text("Provide the names of any 6 programming languages and the app will fetch you the top repositories of these languages, and will plot a graph based on thier stars.",color='black',font_family='karla',text_align='centre',size=16,),
                                height=220,width=335,
                                border_radius=5,
                                alignment= ft.alignment.center,
                                bgcolor="#FFDAB3",
                                padding=12,
                            )
    
    inner_cont = ft.Container(
                            content=ft.Column([heading_cont_1,text_cont_1]),
                            height=280, width=360, 
                            border_radius=5,
                            bgcolor= "#393053",
                            padding=12,
                        )

    create_cont_1 = ft.Container(
                            content=ft.ElevatedButton('Create', on_click=lambda e: pagee.go('/option1'),color='white',),
                            width=80, height=30, 
                            border_radius=5,
                            alignment=ft.alignment.center,
                            # bgcolor=ft.colors.CYAN_100
                        )
    
    outer_cont_1 = ft.Container(
                            content=ft.Column([inner_cont, create_cont_1],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,),
                            width=380, height=350, 
                            border_radius=5,
                            alignment=ft.alignment.center,
                            bgcolor="#393053",
                            padding=10,
                            
                        )

    # Container 2
    heading_cont_2 = ft.Container(
                                content= ft.Text("Single Programming Language.",color='black',size=16,weight='bold',opacity=0.8,),
                                height=30,width=335,
                                border_radius=5,
                                alignment= ft.alignment.center,
                                bgcolor="#FFDAB3",
                            )
    
    text_cont_2  =   ft.Container(
                                content= ft.Text("Name any programming language and the app will fetch you the top 10 github repositories, and will plot a graph based on their stars.",color='black',font_family='karla',size=16,),
                                height=220,width=335,
                                border_radius=5,
                                alignment= ft.alignment.center,
                                bgcolor="#FFDAB3",
                                padding=12,
                            )

    inner_cont_2 = ft.Container(
                            content=ft.Column([heading_cont_2,text_cont_2]),
                            height=280, width=360, border_radius=5,
                            bgcolor= "#393053",
                            padding=12,
                        )

    create_cont_2 = ft.Container(
                            content=ft.ElevatedButton('Create', on_click=lambda e: pagee.go('/option2'),color='white',),
                            width=80, height=30, border_radius=5,
                            alignment=ft.alignment.center,
                            # bgcolor=ft.colors.CYAN_100
                        )
    
    outer_cont_2 = ft.Container(
                            content=ft.Column([inner_cont_2, create_cont_2],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,),
                            width=380, height=350, 
                            border_radius=5,
                            alignment=ft.alignment.center,
                            bgcolor="#393053",
                            padding=10
                        )

    option_cont = ft.Container(
                            content=ft.Text("Choose An Option",
                            color='white'),
                            height=40,width=240,
                            bgcolor='black',
                            border_radius=5,
                            alignment=ft.alignment.center,
                        )

    pagee.update()
    langs=[]
    graph_image = ft.Image(src='assets/blank.png')
    
    def add_lang(e):
            lang = input_text1.value.strip()
            if lang:
                langs.append(lang)
                input_text1.value = ''
                output_text1.value = f"Added: {lang}, languages added: {len(langs)}"
                output_text1.color = "green"
            else:
                output_text1.value = "Please enter a valid language."
                output_text1.color = "red"

            graph_image.src = "src/blank.png"
            
            pagee.update()
    
    def submit(e):
            hyper_text2.spans.clear()
            if not langs:
                output_text1.value = "No languages added. Please add at least one language."
                output_text1.color = "red"
                pagee.update()
                return

            owners, stars, urls, descriptions = [], [], [], []
            for lang in langs:
                try:
                    url = f'https://api.github.com/search/repositories?q=language:{lang}+sort:stars'
                    r = requests.get(url)
                    responses = r.json()
                    repo_dicts = responses['items']

                    for item in repo_dicts:
                        owner = item['owner']['login']
                        star = item['stargazers_count']
                        repo = f"{lang}: {owner}"
                        url = item['owner']['html_url']
                        description = item['description']
                        owners.append(repo)
                        stars.append(star)
                        urls.append(url)
                        descriptions.append(description)
                        break

                except KeyError:
                    output_text1.value = f"Error requesting data for {lang}"
                    output_text1.value += " (Check your spelling)"
                    output_text1.color = "red"
                    pagee.update()
                    return

            
            fig, ax = plt.subplots()
            ax.bar(owners, stars)
            plt.xlabel('Repository')
            plt.ylabel('Stars')
            plt.title('Top Github Repositories by stars')
            fig.autofmt_xdate()
            unique_filename = f"Graph_{uuid.uuid4()}.png"
            plt.savefig(unique_filename)
            plt.close(fig) 

            graph_image.src = unique_filename

            if hasattr(graph_image, 'prev_src') and os.path.exists(graph_image.prev_src):
                    os.remove(graph_image.prev_src)
            
            
            graph_image.prev_src = unique_filename
            output_text1.value = "Graph Generated Successfully!"
            output_text1.color = "green"
            pagee.update()

            hyperlinks_span2 = []

            for i in range(len(owners)):
                hyperlinks_span2.append(
                    ft.TextSpan(
                        owners[i],
                        url=urls[i],
                        style=ft.TextStyle(
                            color="blue",
                            decoration=ft.TextDecoration.UNDERLINE,
                        ),
                    )
                )
                
            for span, description in zip(hyperlinks_span2, descriptions):
                
                hyper_text2.spans.append(span)
                hyper_text2.spans.append(ft.TextSpan("\n"))  

                
                hyper_text2.spans.append(
                    ft.TextSpan(
                        f"Description: {description}\n",  
                        style=ft.TextStyle(color="white"),  
                    )
                )
                hyper_text2.spans.append(ft.TextSpan("\n"))
            langs.clear()
            pagee.update()
    
    input_text2 =ft.TextField(content_padding=2, text_align= ft.TextAlign.CENTER)
    
    def plot(e):
        graph_image.src = "src/blank.png"
        hyper_text1.spans.clear()
        
        language = input_text2.value.strip()
        url = f'https://api.github.com/search/repositories?q=language:{language}+sort:stars'
        r   = requests.get(url)
        reponses = r.json()

        # Defining Variables 
        repo_dicts = reponses['items']
        ownerss, starss, urlss, descriptions = [], [], [], []
        for item in repo_dicts[:10]:
                owner = item['owner']['login']
                star = item['stargazers_count']
                repo = f"{language}: {owner}"
                url = item['owner']['html_url']
                description = item['description']
                ownerss.append(repo)
                starss.append(star)
                urlss.append(url)
                descriptions.append(description)
        
        fig, ax = plt.subplots()
        ax.bar(ownerss, starss)
        plt.xlabel('Repository')
        plt.ylabel('Stars')
        plt.title('Top 10 repositories.')
        fig.autofmt_xdate()

        unique_filename = f"Graph_{uuid.uuid4()}.png"
        plt.savefig(unique_filename)
        plt.close(fig) 

        graph_image.src = unique_filename

        if hasattr(graph_image, 'prev_src') and os.path.exists(graph_image.prev_src):
                os.remove(graph_image.prev_src)
        
        
        graph_image.prev_src = unique_filename

        output_text1.value = "Graph Generated Successfully!"
        output_text1.color = "green"

        hyperlinks_span1 = []

        for i in range(len(ownerss)):
            hyperlinks_span1.append(
                ft.TextSpan(
                    ownerss[i],
                    url=urlss[i],
                    style=ft.TextStyle(
                        color="blue",
                        decoration=ft.TextDecoration.UNDERLINE,
                    ),
                )
            )
            
        for span, description in zip(hyperlinks_span1, descriptions):
            
            hyper_text1.spans.append(span)
            hyper_text1.spans.append(ft.TextSpan("\n"))  

            
            hyper_text1.spans.append(
                ft.TextSpan(
                    f"Description: {description}\n",  
                    style=ft.TextStyle(color="white"),  
                )
            )
            hyper_text1.spans.append(ft.TextSpan("\n"))  

        pagee.update()

    hyper_text1 = ft.Text(spans=[])

    scrollable_content_1 = ft.Column(
                            controls=[hyper_text1],
                            scroll=ft.ScrollMode.AUTO, 
                            expand=True, 
                        )

    hyperlinks1 = ft.Container(
                            content= scrollable_content_1,
                            width= pagee.window.width,
                            height= pagee.window.max_height,
                            bgcolor= "#393053",
                            padding= 10,
                            border_radius=10,
                            expand=True,
                        )

    hyper_text2 = ft.Text(spans=[])

    scrollable_content_2 = ft.Column(
                            controls=[hyper_text2],
                            scroll=ft.ScrollMode.AUTO, 
                            expand=True, 
                        )

    hyperlinks2 = ft.Container(
                            content= scrollable_content_2,
                            width= pagee.window.width,
                            height= pagee.window.max_height,
                            bgcolor= "#393053",
                            padding= 10,
                            border_radius=10,
                            expand=True,
                        )
    pagee.update()
# Button functions.
    def home_route(e):
        pagee.go('/')
        graph_image.src = "assets/blank.png"
        output_text1.value = " "
        langs.clear()
    
    def option1(e):
        pagee.go('/option1')
        graph_image.src = "assets/blank.png"
        output_text1.value = " "
        hyper_text1.spans.clear()
        input_text1.value = " "
        langs.clear()
        
    def option2(e):
        pagee.go('/option2')
        graph_image.src = "assets/blank.png"
        output_text1.value = " "
        hyper_text2.spans.clear()
        input_text2.value = " "
        langs.clear()

# Option 1 variables

    op1_text_cont = ft.Container(
                            content= ft.Text("Please name atmost 6 programming languages"),
                            alignment= ft.alignment.center,
                        )
    
    input_text1 =ft.TextField(content_padding=2, text_align= ft.TextAlign.CENTER)

    op1_row_cont = ft.Container(
                        content=ft.Row(
                            [
                                ft.ElevatedButton("Go Home", on_click= home_route,color='white',),
                                ft.ElevatedButton("Option2", on_click= option2, color='white',)
                            ],ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    )

    op1_input_cont = ft.Container(
                            content=ft.Row(
                        [
                            ft.Container(
                                content=input_text1,
                                width=220,
                                height=30,
                                bgcolor='black',
                                padding=2,
                                border_radius=5,
                                
                                         ),
                            
                            ft.Container(
                                content=ft.Text("add"),
                                width=30,
                                height=30,
                                border_radius=15,
                                on_click=add_lang,
                                         ),
                                        

                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment= ft.CrossAxisAlignment.CENTER
                        ),
                            alignment= ft.alignment.center,
                    )

    op1_plot_cont = ft.Container(
                            content=ft.ElevatedButton("Plot", on_click= submit, color='white',),
                            alignment= ft.alignment.center,
                        )
    
    output_text1 = ft.Text(" ")

    op1_outer_cont = ft.Container(
                            bgcolor="#393053",
                            height=160,
                            width=pagee.window.width,
                            border_radius=10,
                            content=ft.Column([op1_text_cont,op1_input_cont,op1_plot_cont,output_text1,],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER),

                            padding=10,
                            alignment=ft.alignment.center,
                        )

    op1_image_cont = ft.Container(
                                content=graph_image,
                                height= 300,
                                width= pagee.window.width,
                                padding=10,
                            )

# Option 2 Variables

    op2_text_cont = ft.Container(
                            content= ft.Text("Please name any programming language"),
                            alignment= ft.alignment.center,
                        )

    op2_row_cont = ft.Container(
                            content=ft.Row(
                            [
                                ft.ElevatedButton("Go Home", on_click= home_route,color='white',),
                                ft.ElevatedButton("Option1", on_click= option1,color='white',)
                            ], ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                    )

    op2_input_cont = ft.Container(
                                content=input_text2,
                                width=220,
                                height=30,
                                bgcolor='black',
                                padding=2,
                                border_radius=5,
                                alignment= ft.alignment.center,
                            )
                            
    op2_plot_cont = ft.Container(
                            content=ft.ElevatedButton("Plot", on_click= plot,color='white',),
                            alignment= ft.alignment.center,
                        )

    op2_outer_cont = ft.Container(
                            bgcolor="#393053",
                            height=160,
                            width=pagee.window.width,
                            border_radius=10,
                            alignment=ft.alignment.center,
                            content=ft.Column([op2_text_cont,op2_input_cont,op2_plot_cont, output_text1,],
                                    alignment= ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment= ft.CrossAxisAlignment.CENTER),
                            padding=10,
                        )
    
    op2_image_cont = ft.Container(
                            content=graph_image,
                            height= 300,
                            width= pagee.window.width,
                        )

    pagee.update()    
    
    # Routing
    def view_handler(route):
        views =  {
            '/':ft.View(
                route='/',
                appbar= ft.AppBar(title=ft.Text('Genesis'),center_title=True,),
                controls=[
                    
                    ft.Container(height=pagee.window.height,width=pagee.window.width,
                                bgcolor="#18122B",            
                                content=ft.Column(
                                        [option_cont,outer_cont_1,outer_cont_2],
                                        # alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        scroll= ft.ScrollMode.AUTO,
                                        expand=True,
                                        ),
                                border_radius=10,
                                expand=True,
                                padding=10,
                                ),                    
                ],
                fullscreen_dialog= True,
                
            ),

            '/option1':ft.View(
                    route='/option1',
                    appbar= ft.AppBar(title=ft.Text('Genesis'),center_title=True,),
                    controls=[
                        
                        
                        ft.Container(content=ft.Column([op1_row_cont,op1_outer_cont,op1_image_cont, hyperlinks2], auto_scroll=True),
                                     alignment=ft.alignment.center,
                                     expand=True,
                                     bgcolor="#18122B",
                                     width=pagee.window.width,
                                     height=pagee.window.height,)

                    ],
                    fullscreen_dialog= True,
                    
            ),

            '/option2':ft.View(
                    route='/option2',
                    appbar= ft.AppBar(title=ft.Text('Genesis'),center_title=True,),
                    controls=[
                        
                        ft.Container(content=ft.Column([op2_row_cont,op2_outer_cont,op2_image_cont,hyperlinks1], auto_scroll=True),
                        alignment=ft.alignment.center,
                        expand=True,
                        bgcolor="#18122B",
                        width=pagee.window.width,
                        height=pagee.window.height)
                    ],
                    fullscreen_dialog= True,
                    
            ),

        }
        pagee.update()
        return views.get(route)
        
    
    def route_change(e):
        pagee.views.clear()
        view = view_handler(pagee.route)
        if view:
            pagee.views.append(view)
        pagee.update()

    
    pagee.update()
    pagee.on_route_change = route_change
    pagee.go('/')
    pagee.update()

ft.app(target=main, assets_dir="assets")