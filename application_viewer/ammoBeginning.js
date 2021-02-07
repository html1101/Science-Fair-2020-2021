// const Ammo = require("./ammo");
// Working from this guide: https://medium.com/@bluemagnificent/intro-to-javascript-3d-physics-using-ammo-js-and-three-js-dd48df81f591

let physicsWorld, scene, camera, renderer;
/**
 * RigidBodies: array for all Three.js mesh(.userData.physicsBody contains info about the AmmoJS body)
 * tmpTrans: a temporary ammo.js transform object
 */
let rigidBodies = [], tmpTrans, defaultMargin = 0.05;

// For bit masking
let colGroupPlane = 1,
colGroupRedBall = 2,
colGroupGreenBall = 4
Ammo().then(() => {
    tmpTrans = new Ammo.btTransform()
    setupPhysicsWorld()

    setupGraphics()
    
    createBlock()
    for(let i = 0; i < 100; i++) {
        createBall(pos={
            x: (i % 10)*2,
            y: (i % 10)*2,
            z: 0
        },
        ballType=2*(1+i%2),
        mass=4)
    }

    renderFrame()
})

/**Sets up simple physics world for simulation */
const setupPhysicsWorld = () => {
    // Sets up simple physics world for simulation
    let collisionConfiguration = new Ammo.btDefaultCollisionConfiguration(), // Default collision detection
        dispatcher = new Ammo.btCollisionDispatcher(collisionConfiguration), // Default collision dispatcher
        overlappingPairCache = new Ammo.btDbvtBroadphase(), // Broadphase algorithm to use
        solver = new Ammo.btSequentialImpulseConstraintSolver() // Allows objects to interact properly

    physicsWorld = new Ammo.btDiscreteDynamicsWorld(dispatcher, overlappingPairCache) // Dynamic world
    physicsWorld.setGravity(new Ammo.btVector3(0, -15, 0))
}

const setupGraphics = () => {
    // Clock for timing
    clock = new THREE.Clock()

    // New THREE.js scene and set background
    scene = new THREE.Scene()
    scene.background = new THREE.Color(0xbfd1e5)

    // Create camera, position it at [0, 30, 70], and have it pointing at position [0, 0, 0]
    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.2, 5000)
    camera.position.set(0, 30, 70)
    camera.lookAt(new THREE.Vector3(0, 0, 0))

    // Add hemisphere light
    let hemisLight = new THREE.HemisphereLight(0xffffff, 0xffffff, 0.1)
    hemisLight.color.setHSL(0.6, 0.6, 0.6)
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

    // Setup the renderer
    renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setClearColor(0xbfd1e5)
    renderer.setPixelRatio(window.devicePixelRatio)
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)
    
    renderer.gammaInput = true;
    renderer.gammaOutput = true;

    // Initializes OrbitControls
    const orbitControls = new THREE.OrbitControls(camera, renderer.domElement) 

    // Render scene from light's POV and everything from light's perspective is lit up
    renderer.shadowMap.enabled = true
}

const renderFrame = () => {
    requestAnimationFrame(renderFrame)
    let deltaTime = clock.getDelta()
    
    updatePhysics(deltaTime)

    renderer.render(scene, camera)
}

const createBlock = (pos = { x: 0, y: 0, z: 0 }, size = { x: 50, y: 2, z: 50 }) => {
    let rot = { x: 0, y: 0, z: 0, w: 1 },
        mass = 0 // Infinite mass, therefore static

    // ThreeJS box
    let blockPlane = new THREE.Mesh(
        new THREE.BoxBufferGeometry(),
        new THREE.MeshPhongMaterial({ color: 0xa0afa4 })
    )

    blockPlane.position.set(pos.x, pos.y, pos.z)
    blockPlane.scale.set(size.x, size.y, size.z)

    blockPlane.castShadow = true
    blockPlane.receiveShadow = true

    scene.add(blockPlane)

    // Ammo.js: setting up vector quaternion & position
    let transform = new Ammo.btTransform() // Used to transform points from one coordinate space into another
    transform.setIdentity()
    transform.setOrigin(new Ammo.btVector3(pos.x, pos.y, pos.z))
    transform.setRotation(new Ammo.btQuaternion(rot.x, rot.y, rot.z, rot.w))
    let motionState = new Ammo.btDefaultMotionState(transform)

    // Ammo.js: setting up box
    let colShape = new Ammo.btBoxShape(new Ammo.btVector3(size.x * 0.5, size.y * 0.5, size.z * 0.5))
    colShape.setMargin(defaultMargin) // Small collision margin to improve performance

    // Setting inertia
    let localInertia = new Ammo.btVector3(0, 0, 0)
    colShape.calculateLocalInertia(mass, localInertia)

    // Creating the Ammo RigidBody
    /** Ammo RigidBody requires:
     * mass,
     * motionState(we will use the default for this and input our transformation vector), 
     * the actual box/body(which we add a margin to)
     * localInertia(a vector containing the body's inertia)
     */
    let rbInfo = new Ammo.btRigidBodyConstructionInfo(mass, motionState, colShape, localInertia),
        body = new Ammo.btRigidBody(rbInfo)

    physicsWorld.addRigidBody(body, colGroupPlane, colGroupRedBall)
}

const createBall = (pos = { x: 0, y: 20, z: 0 }, ballType=1, radius = 2, mass = 1) => {
    let rot = { x: 0, y: 0, z: 0, w: 1 } // Note: w = cos(theta / 2), w=1 means 0 rotation angle around an undefined axis
    console.log(ballType)

    // ThreeJS ball
    let ball = new THREE.Mesh(
        new THREE.SphereBufferGeometry(radius),
        new THREE.MeshPhongMaterial({ color: (ballType == colGroupGreenBall) ? 0x05ff05 : 0xff0505 })
    )

    ball.position.set(pos.x, pos.y, pos.z)

    ball.castShadow = true
    ball.receiveShadow = true

    scene.add(ball)

    // AmmoJS: setting up vector position and quaternion
    let transform = new Ammo.btTransform()
    transform.setIdentity()
    transform.setOrigin(new Ammo.btVector3(pos.x, pos.y, pos.z))
    transform.setRotation(new Ammo.btQuaternion(rot.x, rot.y, rot.z, rot.w))
    let motionState = new Ammo.btDefaultMotionState(transform)

    // AmmoJS: Sphere
    let colShape = new Ammo.btSphereShape(radius)
    colShape.setMargin(0.05)

    // AmmoJS: Inertia
    let localInertia = new Ammo.btVector3(0, 0, 0)
    colShape.calculateLocalInertia(mass, localInertia)

    let rbInfo = new Ammo.btRigidBodyConstructionInfo(mass, motionState, colShape, localInertia),
        body = new Ammo.btRigidBody(rbInfo)

    if(ballType == colGroupRedBall) {
        physicsWorld.addRigidBody(body, colGroupRedBall, colGroupPlane | colGroupGreenBall | colGroupRedBall)
    } else {
        physicsWorld.addRigidBody(body, colGroupGreenBall, colGroupRedBall | colGroupGreenBall)
    }
    

    // Add to rigidBodies array
    ball.userData.physicsBody = body
    rigidBodies.push(ball)
}

const updatePhysics = (deltaTime) => {
    // Step world
    physicsWorld.stepSimulation(deltaTime*5, 10) // 10 is the max # of simulation steps within a fixed framerate

    // Update the rigid bodies
    for (let i = 0; i < rigidBodies.length; i++) {
        let objThree = rigidBodies[i],
            objAmmo = objThree.userData.physicsBody,
            ms = objAmmo.getMotionState()

        if (ms) {
            ms.getWorldTransform(tmpTrans)
            let p = tmpTrans.getOrigin(),
                q = tmpTrans.getRotation()
            objThree.position.set(p.x(), p.y(), p.z())
            objThree.quaternion.set(q.x(), q.y(), q.z(), q.w())
        }
    }
}
