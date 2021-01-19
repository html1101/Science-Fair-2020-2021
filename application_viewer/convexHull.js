/**
 * Steps:
 * Initialize Ammo.js(setupPhysicsWorld)
 * Initialize THREE.js(setupGraphics)
 * Create class to manage PDB files(loadMol)
 * Load the PDB file(loadPDB)
 * Identify which chains are light, heavy, and not a part of the antibody(will be assumed to be a part of the antigen)(detectChains)
 * Render them
 * Group them together(initially attempt with joints, if it doesn't work move on to creating custom meshes)
 * Pull them towards the epitopes(initially explicitly specify)
 * Create a genetic algorithm
*/

let physicsWorld, scene, camera, renderer, controls;
/**
 * RigidBodies: array for all Three.js mesh(.userData.physicsBody contains info about the AmmoJS body)
 * tmpTrans: a temporary AmmoJS transform object
 * tmpVec: a temporary AmmoJS vector
 * defaultMargin: The margin for error for AmmoJS(padding)
 * molecules: Holds a list of the atom classes
 * antigenChains: The chains associated with the antigen being targeted
*/
let rigidBodies = [],
tmpTrans,
tmpVec,
defaultMargin = 0.05,
molecules = [],
antigen_chains = ["A", "C", "E", "B", "D", "F"] // For debugging, this will be explicitly set for the specific molecule we're working with.

// For bit masking(what will collide with what)
let colGroupAntigen = 1,
    colGroupAntibody = 2,
    colGroupGreenBall = 4

// Deals with rendering after Ammo has been loaded
Ammo().then(() => {
    tmpTrans = new Ammo.btTransform()
    tmpVec = new Ammo.btVector3()
    setupPhysicsWorld()

    setupGraphics()

    renderFrame()
})

// Initialize Ammo.js
const setupPhysicsWorld = () => {
    // Setup simple physics world for simulation

    let collisionConfiguration = new Ammo.btDefaultCollisionConfiguration(), // Default collision detector
        dispatcher = new Ammo.btCollisionDispatcher(collisionConfiguration),
        overlappingPairCache = new Ammo.btDbvtBroadphase(), // Binary tree broadphase algorithm to use
        solver = new Ammo.btSequentialImpulseConstraintSolver() // Allows objects to interact properly
        

    physicsWorld = new Ammo.btDiscreteDynamicsWorld(dispatcher, overlappingPairCache) // Dynamic world
    physicsWorld.setGravity(new Ammo.btVector3(0, 0, 0))
}

// Initialize THREE.js
const setupGraphics = () => {
    // Clock to manage AmmoJS physic steps
    clock = new THREE.Clock()

    // New THREE.js scene and setting up background
    scene = new THREE.Scene()
    scene.background = new THREE.Color(0xbfd1e5)

    // Create camera, position it at [0, 30, 70], and have it pointing at [0, 0, 0]
    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.2, 5000) // fov, aspect, near, far
    camera.position.set(0, 30, 70)
    camera.lookAt(new THREE.Vector3(0, 0, 0))

    // Add hemisphere lighting
    let hemisLight = new THREE.HemisphereLight(0xffffff, 0xffffff, 0.1)
    hemisLight.color.setHSL(0.6, 0.6, 0.6) // Blue?
    hemisLight.groundColor.setHSL(0.1, 1, 0.4)
    hemisLight.position.set(0, 50, 0)
    scene.add(hemisLight)

    // Add directional light
    let dirLight = new THREE.DirectionalLight(0xffffff, 1)
    dirLight.color.setHSL(0.1, 1, 0.95)
    dirLight.position.set(-1, 1.75, 1)
    dirLight.position.multiplyScalar(100)
    scene.add(dirLight)

    dirLight.castShadow = true

    // Set directional lighting width and height of the shadow
    dirLight.shadow.mapSize.width = 2048
    dirLight.shadow.mapSize.height = 2048

    // Set shadow positioning
    let d = 50
    dirLight.shadow.camera.left = -d
    dirLight.shadow.camera.right = d
    dirLight.shadow.camera.top = d
    dirLight.shadow.camera.bottom = -d

    dirLight.shadow.camera.far = 13500

    // Setup renderer
    renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setPixelRatio(window.devicePixelRadio)
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    // renderer.gammaInput = true
    // renderer.gammaOutput = true

    // Setup OrbitControls(allows panning, moving around camera)
    controls = new THREE.OrbitControls(camera, renderer.domElement)

    // Render scene from light's POV and everything from light's perspective is lit up.
    renderer.shadowMap.enabled = true
}


// Load PDB file
let file_load = document.getElementById("pdb"),
fr = new FileReader(),
avg_antibody = [0, 0, 0],
avg_antigen = [0, 0, 0],
antibody_count = 0,
antigen_count = 0 // Number of antigen atoms in the PDB
const loadPDB = () => {
    fr.onload = () => {
        let val = fr.result.split("\n").filter(x => {
            return x.slice(0, 4) == "ATOM"
        }) // The result of loading the file, filtered by atom(takes out header, remark lines, etc)
        for(let i = 0; i < val.length; i++) {
            console.log(val[i])
        }
    
        // Setup camera
        camera.position.set(avg_antibody[0] - 20, avg_antibody[1], avg_antibody[2] - 20)
        camera.lookAt(new THREE.Vector3(avg_antibody[0], avg_antibody[1], avg_antibody[2]))
        controls.target = new THREE.Vector3(avg_antibody[0], avg_antibody[1], avg_antibody[2])
        controls.update()

        renderFrame()
    }
    fr.readAsText(file_load.files[0])
}
file_load.addEventListener("change", loadPDB)

// Step forward in AmmoJS world
const updatePhysics = (deltaTime) => {
    // Step world
    physicsWorld.stepSimulation(deltaTime*20, 10) // (time in ms passed, the max # of simulation steps within a fixed framerate)

    // Update the rigid bodies
    for(let i = 0; i < molecules.length; i++) {
        if(!molecules[i].is_antigen_chain) { // Apply velocity
            molecules[i].update()
            // tmpVec.setValue(linear_pos)
            molecules[i].mol.userData.physicsBody.setLinearVelocity(tmpVec)
        }
    }
}

// Manage rendering process
const renderFrame = () => {
    requestAnimationFrame(renderFrame)
    let deltaTime = clock.getDelta()

    updatePhysics(deltaTime)

    renderer.render(scene, camera)
}