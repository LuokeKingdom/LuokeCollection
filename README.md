<p align="center">
<a href="https://github.com/LuokeKingdom/LuokeCollection/projects/1">
<img align="center" src="https://user-images.githubusercontent.com/55712285/178427638-626dd05c-06fc-46ac-83b2-8a76bff98443.png" width="200"/>
</a>
</p>

# LuokeCollection 洛克王國 寵物圖鑑
![Tests](https://github.com/LuokeKingdom/LuokeCollection/actions/workflows/ci.yml/badge.svg)

This project aims to recreate a PET index of the game Roco Kingdom

## In-game Screenshot
![In-game Screenshot](https://user-images.githubusercontent.com/55712285/178428547-2d43b702-726f-4df1-aa74-60519304d84b.png)
## Instructions
* To run: `make` or `make run`
* To reformat: `make black`
* To bump the version of the project: `make versoin major/minor/patch` 

## Custom Scene
- create new `custom_view.py` file in `LuokeCollection/main/scenes/views`
    - inherit from `View` class
    - see `init_view.py` for reference
- create new `custom_controller.py` file in `LuokeCollection/main/scenes/controller`
    - inherit from `Controller` class
    - see `init_controller.py` for reference
- add your new scenes to the `TABLE` in `LuokeCollection/main/scenes/scene.py`
- call `app.change_scene('your scene name')` to visualize your scene.

# View
- Components:
    - Background: just a static image for now
    - Button: 
        - put your buttons in the `BUTTONS` as (name, Button) pairs
        - should be linked with an `on_click` function in its controller class
    - Text: to be announced
    - Sprite: to be announced

# Controller
- self.actions:
    - map the button name and on_click function here for now