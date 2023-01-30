# Import javascript modules
import imaplib
import imghdr
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math


#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    # Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0xF0EEE9)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 15
    scene.add(camera)

    # Directional light
    color = 0xFFFFFF
    intensity = 1
    light = THREE.DirectionalLight.new(color, intensity)
    light.position.set(0, 1, 0)
    scene.add(light)

    # Spotlight
    spotLight = THREE.SpotLight.new(color, intensity)
    spotLight.position.set(0, 1, 0)
    spotLight.target.position.set(0, 0, 0)
    scene.add(spotLight)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
  
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)
    # Axis Helper
    axesHelper = THREE.AxesHelper.new(100)
    scene.add(axesHelper)
    #-----------------------------------------------------------------------
    # Set up GUI

    floor_length_x = 10
    floor_length_y = 8
    floor_ratio = 1/2
    floor_iterations = 2

    floorsettings = {
        "length_x": floor_length_x,
        "length_y": floor_length_y,
        "public_private": floor_ratio,
        "public_private": floor_ratio,
    }
    floorsettings = Object.fromEntries(to_js(floorsettings))

    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Floor Settings')
    param_folder.add(floorsettings,'length_x', 1,20,1)
    param_folder.add(floorsettings,'length_y', 1,20,1)
    param_folder.add(floorsettings,'public_private', 0.2,0.7)
    param_folder.add(floorsettings,'public_private', 0.2,0.7)
    
    param_folder.open()

    #-----------------------------------------------------------------------
    # Create Materials
    # Mesh Material
    global material, line_material
    material = THREE.MeshBasicMaterial.new()
    material.color = THREE.Color.new(0xA32A8C)
    material.transparent = True
    material.opacity = 0.6

    # Line Material
    line_material = THREE.LineBasicMaterial.new()
    line_material.color = THREE.Color.new(0x1B1B1B)
    #-----------------------------------------------------------------------
    # Lists
    global final_rooms, lines, new_rooms, offset_rooms, shapes
    #Roomlists
    # rooms = [room_1, room_2, ..., room_n] room_n = [point_1, point_2, point_3, point_4]
    final_rooms = []
    lines = []
    new_rooms = []
    offset_rooms = []
    shapes = []
    

    # Impliment 
    # Original room
    firstroom = define_room(0, 0, floorsettings.length_x, 0, floorsettings.length_x , floorsettings.length_y, 0, floorsettings.length_y)
    new_rooms.append(firstroom)



    #Apartements

    Apartement(2,1,[1/2, 1/3, 3/4, 0, 0, 0, 2/3, 0, 0])

    #offset rooms for Wall vertices
    offset_out(new_rooms[0], 0.2)
    offset_in(final_rooms, 0.1)
    
    drawrooms(offset_rooms)
    extrude(firstroom, offset_rooms)
    

    render()
#-----------------------------------------------------------------------
# HELPER FUNCTIONS

#GUI function
def GUI():
    global floorsettings, floor_length_x, floor_length_y, floor_iterations, floor_ratio

    floor_length_x = 10
    floor_length_y = 12
    floor_ratio = 1/2
    floor_iterations = 2

    floorsettings = {
        "length_x": floor_length_x,
        "length_y": floor_length_y,
        "public_private": floor_ratio,
        "public_private": floor_ratio,
    }
    floorsettings = Object.fromEntries(to_js(floorsettings))

    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Floor Settings')
    param_folder.add(floorsettings,'length_x', 1,20,1)
    param_folder.add(floorsettings,'length_y', 1,20,1)
    param_folder.add(floorsettings,'public_private', 0.2,0.7)
    param_folder.add(floorsettings,'public_private', 0.2,0.7)
    
    param_folder.open()


# Apartement function
def Apartement(apartement_type, number, ratios):

    if apartement_type == 1:
        Apartement_1(number,ratios)
    elif apartement_type == 2:
         Apartement_2(number,ratios)
    elif apartement_type == 3:
         Apartement_3(number,ratios)
    pass

# Apartement variation functions
def Apartement_1(number,ratios):
    if number == 1:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],ratios)
    elif number == 2:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],ratios)
    elif number == 3:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],ratios)
    elif number == 4:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],ratios)
    elif number == 5:
        variante(['V', 'V', 'H', 0, 0, 0, 'H', 0, 0],ratios)
    pass

def Apartement_2(number,ratios):
    if number == 1:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],ratios)
    elif number == 2:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],ratios)
    elif number == 3:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],ratios)
    elif number == 4:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],ratios)
    elif number == 5:
        variante(['V', 'V', 'H', 0, 0, 0, 'H', 0, 0],ratios)
    pass

def Apartement_3(number,ratios):
    if number == 1:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],ratios)
    elif number == 2:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],ratios)
    elif number == 3:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],ratios)
    elif number == 4:
        variante(['V', 'H', 'V', 0, 0, 0, 'H', 0, 0],ratios)
    elif number == 5:
        variante(['V', 'V', 'H', 0, 0, 0, 'H', 0, 0],ratios)
    pass

# room definition
def define_room(p1_x, p1_y, p2_x, p2_y, p3_x, p3_y, p4_x, p4_y):
    room = []
    p1 = p1_x, p1_y
    p2 = p2_x, p2_y
    p3 = p3_x, p3_y
    p4 = p4_x, p4_y
    room.append(p1)
    room.append(p2) 
    room.append(p3) 
    room.append(p4)
    return room

# draw rooms
def drawrooms(rooms):

    
    for line in lines:
        scene.remove(line)

    for room in rooms:
        points = []
        point1 = THREE.Vector2.new(room[0][0],room[0][1])
        point2 = THREE.Vector2.new(room[1][0],room[1][1])
        point3 = THREE.Vector2.new(room[2][0],room[2][1])
        point4 = THREE.Vector2.new(room[3][0],room[3][1])

        points.append(point1)
        points.append(point2)
        points.append(point3)
        points.append(point4)
        points.append(point1)

        line_geometry = THREE.BufferGeometry.new()
        line_geometry.setFromPoints(to_js(points))
        line = THREE.Line.new(line_geometry, line_material)
        lines.append(line)
        scene.add(line)

# extrude Shape

def extrude(boundary, rooms):
    shape_geometry = THREE.Shape.new()
    #boundary extrusion
    shape_geometry.moveTo(boundary[0][0],boundary[0][1])
    shape_geometry.lineTo(boundary[1][0],boundary[1][1])
    shape_geometry.lineTo(boundary[2][0],boundary[2][1])
    shape_geometry.lineTo(boundary[3][0],boundary[3][1])
    shape_geometry.lineTo(boundary[0][0],boundary[0][1])

    #holes

    for room in rooms:

        room_hole = THREE.Path.new()
        
        room_hole.moveTo(room[0][0],room[0][1])
        room_hole.lineTo(room[1][0],room[1][1])
        room_hole.lineTo(room[2][0],room[2][1])
        room_hole.lineTo(room[3][0],room[3][1])
        room_hole.lineTo(room[0][0],room[0][1])

        shape_geometry.holes.push(room_hole)

    
    extrudeSettings = (1,1,False,0,0,0,0)

    '''extrudeSettings = {
	steps: 200,
	depth: 1600,
	bevelEnabled: False,
	bevelThickness: 1,
	bevelSize: 1,
	bevelOffset: 0,
	bevelSegments: 1
    }'''
    

    geometry = THREE.ExtrudeGeometry.new( shape_geometry, extrudeSettings)
    mesh = THREE.Mesh.new(geometry, material)
    scene.add(mesh)


#offset room inside function by changing the vertices
def offset_in(rooms, d):
    global new_rooms, offset_rooms
    for room in rooms:
        offset_room = define_room(room[0][0] + d , room[0][1] + d , room[1][0] - d , room[1][1] + d , room[2][0] - d , room [2][1] - d, room[3][0] + d, room[3][1] - d)
        offset_rooms.append(offset_room)

#offset room outside function by changing the vertices
def offset_out(room, d):
    global new_rooms, offset_rooms
    offset_room = define_room(room[0][0] - d , room[0][1] - d , room[1][0] + d , room[1][1] - d , room[2][0] + d , room [2][1] + d, room[3][0] - d, room[3][1] + d)
    offset_rooms.append(offset_room)



# tree function for room variants      
def variante(syntax, ratios):
    
    index = -1
    for letter in syntax:
        index +=1
        if letter == 'V':
            subdivide_vertical(new_rooms[index], ratios[index])
        elif letter == 'H':
            subdivide_horizontal(new_rooms[index], ratios[index])
        else:
            pass
            final_rooms.append(new_rooms[index])

# Function to subdivide a room vertically
def subdivide_vertical(room, ratio):
    global new_rooms
    new_room1 = define_room(room[0][0], room[0][1], room[1][0] - ((room[1][0]-room[0][0]) * ratio), room[1][1], room[2][0] - ((room[2][0]-room[3][0]) * ratio), room[2][1], room[3][0], room[3][1])
    new_room2 = define_room(room[1][0] - ((room[1][0]-room[0][0]) * ratio), room[0][1], room[1][0], room[1][1], room[2][0], room[2][1], room[2][0] - ((room[2][0]-room[3][0]) * ratio), room[3][1])
    new_rooms.append(new_room1)
    new_rooms.append(new_room2)
#next steps


# Function to subdivide a room horizontally
def subdivide_horizontal(room, ratio):
    global new_rooms
    new_room1 = define_room(room[0][0], room[0][1], room[1][0], room[1][1], room[2][0], room [2][1] - ((room [2][1] - room [1][1]) * ratio), room[3][0], room[3][1] - (room[3][1] - room[0][1])* ratio)
    new_room2 = define_room(room[0][0], room[3][1] - ((room[3][1] - room[0][1]) * ratio), room[1][0], room[2][1] - ((room[2][1] - room[1][1]) * ratio), room[2][0], room[2][1], room[3][0], room[3][1])
    new_rooms.append(new_room1)
    new_rooms.append(new_room2)

#-----------------------------------------------------------------------------------

#NEXT STEPS
# write symbol syntax to tell how to subdivide a room --> different layout types depending on the syntax
# add different syntaxes

#make walls moveable and deleteable in the UI
#gumball move


#OPEN QUESTIONS
#Number of Rooms follows boundary size?
#How to add doors

#-----------------------------------------------------------------------------------


# update
def update():
    global original_room, floor_length_x, floor_length_y, floor_ratio, floor_iterations

    if floorsettings.length_x != floor_length_x or floorsettings.length_y != floor_length_y:
        original_room = []
        floor_length_x = floorsettings.length_x
        floor_length_y = floorsettings.length_y

        update_room = define_room(-0.5*floorsettings.length_x, -0.5*floorsettings.length_y, 0.5*floorsettings.length_x, -0.5*floorsettings.length_y, 0.5*floorsettings.length_x , 0.5*floorsettings.length_y, -0.5*floorsettings.length_x, 0.5*floorsettings.length_y)
        original_room.append(update_room)
        subdivide_vertical(original_room, floorsettings.public_private)
        subdivide_horizontal(new_rooms, floorsettings.public_private)
        drawrooms(new_rooms)

    '''elif floorsettings.public_private != floor_ratio or floorsettings.iterations != floor_iterations:
        floor_ratio = floorsettings.public_private
        floor_iterations = floorsettings.iterations

        subdivide_vertical(original_room, floorsettings.public_private)
        subdivide_horizontal(new_rooms, floorsettings.public_private)
        drawrooms(new_rooms)'''

    '''else:'''
    pass
        
# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    #update()
    controls.update()
    composer.render()

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()


