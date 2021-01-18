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

// Manage PDB files with class
class loadMol {
    /** Setup loadMol
     * @param line The line containing the information about the atom being rendered
     * @param n The line number we can use for labelling
     * @param typeRendered The way the atom will be rendered(ball, box)
     */
    constructor(line, n, typeRendered = "ball") {
        /**
         * Positions 30-38: x value
         * Positions 38-46: y value
         * Positions 46-54: z value
         */
        this.x = Number(line.slice(30, 38))
        this.y = Number(line.slice(38, 46))
        this.z = Number(line.slice(46, 54))
        this.posArr = [this.x, this.y, this.z]
        this.typeRendered = typeRendered

        // Antigen + chain labeling
        this.chain = line.slice(21, 22)
        this.is_antigen_chain = antigen_chains.includes(this.chain)
        this.name = ((this.is_antigen_chain ? "antigen_" : "antibody_") + n) // Creates label
        this.colGroup = (this.is_antigen_chain + 1)*2
    }
    /** Translates the molecule; needs to be performed before rendering
     * @param x X value to translate by
     * @param y Y value to translate by
     * @param z Z value to translate by
     */
    translate(x, y, z) {
        this.x += x
        this.y += y
        this.z += z
    }
    /** Render the atom given this.x, this.y, this.z
     * @param size Optional parameter - the size of the atom, auto 5
     * @param rot Optional parameter - the rotation of the mesh, auto [0, 0, 0]
     *            Note: w = cos(theta / 2), w=1 means 0 rotation angle around an undefined axis
     */
    render(size = 5, rot = { x: 0, y: 0, z: 0, w: 1}, pos = {x: 0, y: 0, z: 0}) {
        let mass = !this.is_antigen_chain // A mass of 0 = mass of infinity, therefore they are fixed and do not move

        // Setup THREE.js mesh
          this.mol = new THREE.Mesh( // FIX
            new THREE.SphereGeometry(size, 20),
            new THREE.MeshPhongMaterial({ color: (this.is_antigen_chain ? 0xff0000 : 0x00ffff)})
        )

        this.mol.position.set(this.x, this.y, this.z)

        this.mol.castShadow = true
        this.mol.receiveShadow = true

        scene.add(this.mol)

        // AmmoJS: setting up vector positon and quaternion
        let transform = new Ammo.btTransform() // Used to transform points from one coordinate space to another
        transform.setIdentity()
        transform.setOrigin(new Ammo.btVector3(this.x, this.y, this.z))
        transform.setRotation(new Ammo.btQuaternion(rot.x, rot.y, rot.z, rot.w))
        let motionState = new Ammo.btDefaultMotionState(transform)

        // AmmoJS: Sphere
        let colShape = new Ammo.btSphereShape(size)
        colShape.setMargin(defaultMargin) // defaultMargin

        // AmmoJS: Inertia
        let localInertia = new Ammo.btVector3(0, 0, 0)
        colShape.calculateLocalInertia(mass, localInertia)

        let rbInfo = new Ammo.btRigidBodyConstructionInfo(mass, motionState, colShape, localInertia),
        body = new Ammo.btRigidBody(rbInfo)
        
        // addRigidBody(body, collision group it's a part of, collision groups it collides with joined by |)
        physicsWorld.addRigidBody(body)

        // Add to rigidBodies array
        this.mol.userData.physicsBody = body
        rigidBodies.push(this.mol)
    }
    /**Sync the atom's physics engine and THREE.js layers. */
    update() {
        let objThree = this.mol,
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
            molecules.push(new loadMol(val[i], i))
            if(!molecules[molecules.length - 1].is_antigen_chain) {
                // Move molecule
                molecules[molecules.length - 1].translate(-50, -50, -50)
                antibody_count++
                avg_antibody = [molecules[molecules.length - 1].x + avg_antibody[0], molecules[molecules.length - 1].y + avg_antibody[1], molecules[molecules.length - 1].z + avg_antibody[2]]
            } else {
                antigen_count++
                avg_antigen = [molecules[molecules.length - 1].x + avg_antigen[0], molecules[molecules.length - 1].y + avg_antigen[1], molecules[molecules.length - 1].z + avg_antigen[2]]
            }
            molecules[molecules.length - 1].render()
            // molecules[molecules.length - 1].update()
        }
        
        /**
         * Calculate the average position of both the antigen and antibody,
         * We will use this to find the direction the antibody is from the antigen
         * And where we should place the camera.
         */ 
        console.log(avg_antigen, avg_antibody)
        avg_antigen = avg_antigen.map(val => {
            return val / antigen_count
        })
        avg_antibody = avg_antibody.map(val => {
            return val / antibody_count
        })
        
        // Use this to find the direction
        console.log(new THREE.Vector3(...avg_antibody), new THREE.Vector3(...avg_antigen))
        tmpVec.setValue(...new THREE.Vector3(...avg_antibody).sub(new THREE.Vector3(...avg_antigen)).normalize().multiplyScalar(-1).toArray())
        console.log(tmpVec)
        /**
         * arccos[(xa * xb + ya * yb + za * zb) / (√(xa2 + ya2 + za2) * √(xb2 + yb2 + zb2))]
         */
        
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