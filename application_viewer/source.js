// Start by initializing simple THREE.js scene, camera, etc.
const scene = new THREE.Scene(),
camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
camera.position.z = -200
camera.position.y = -200
camera.position.y = -200

// Rendering
const renderer = new THREE.WebGLRenderer()
renderer.setSize(window.innerWidth, window.innerHeight)
// Add to document as canvas element
document.body.appendChild(renderer.domElement)

// Initialize OIMO World
let world = new OIMO.World({
    info: false,
    broadphase: 2,
    gravity: [0, 0, 0]
})

// Orbit controls; these let the user pan/move in the 3D environment.
const controls = new THREE.OrbitControls(camera, renderer.domElement)
// controls.enableKeys = false

// Creating a class for which we can handle our molecules
antigen_chains = ["A", "C", "E", "B", "D", "F"]
class Molecule {
    /** Given a line from the .pdb file, construct the corresponding molecule. */
    constructor(line) {
        // Positions 30-39: x value
        // Positions 39-46: y value
        // Positions 46-55: z value
        this.original_strand = line // For debugging purposes
        this.x = Number(line.slice(30, 38))
        this.y = Number(line.slice(38, 46))
        this.z = Number(line.slice(46, 55))
        // Is it an antigen?
        // If it is, it'll be part of chains A, C, E, B, D, or F. At least for this molecule.
        this.chain = line.slice(21, 22)
        this.is_antigen_chain = antigen_chains.includes(this.chain)
    }
    /** Render the molecule given x, y, and z. If it's an antigen, it remains fixed. If not, it can move around. */
    render(size=5) {
        this.OIMO_mol = world.add({
            type: "sphere",
            size: [size, size, size],
            belongsTo: 1 << this.is_antigen_chain,
            pos: [this.x, this.y, this.z],
            move: !this.is_antigen_chain,
            collidesWith: 0xffffff & ~(1 << this.is_antigen_chain)
        })
        let mat = new THREE.MeshStandardMaterial({
            color: (this.is_antigen_chain ? 0x00ffff : (this.chain == "G" || this.chain == "I" || this.chain == "K" ? 0xff0000 : 0xbb0000)) // Dark red is heavy chain, light red is light chain
        })
        this.THREE_mol = new THREE.Mesh(new THREE.SphereGeometry(size, 20), mat)
        scene.add(this.THREE_mol)
    }
    /**Sync the molecule's OIMO and THREE.js layers. */
    update() {
        /**
         * How copying pos and quat work:
         * box[three.js version].position.copy(box[OIMO version].getPosition())
         * box[three.js version].quaternion.copy(box[OIMO version].getQuaternion())
         */
        this.THREE_mol.position.copy(this.OIMO_mol.getPosition())
        this.THREE_mol.quaternion.copy(this.OIMO_mol.getQuaternion())
    }
    translate(x, y, z) {
        // Translates the molecule; we will use this so that we can separate the antigen and antibodies.
        // This needs to be performed before rendering.
        this.x += x
        this.y += y
        this.z += z
    }
    /**
     * Given the position to which the molecule will be pulled, applyImpulse using OIMO.
     * @constructor
     * @param {Array.<number>} pos - The position the molecule will be drawn to.
     */
    applyForce(pos) {
        let center = new THREE.Vector3(-200, -200, -200), // Converting to 3D THREE Vector, which is compatible with OIMO.
            force = this.THREE_mol.position.clone().negate().normalize().multiplyScalar(70) // The force it's going to be pulled towards that point
        // console.log(force)
        this.OIMO_mol.applyImpulse(center, force)
    }
}

// Now that we've created the framework with which to initialize the molecules, we can load the full file.
molecules = [], // List of molecules
avgPoint = [0, 0, 0], // Average point for where we're going to place the magnet. This is purely for testing right now.
num_antigen = 0 // Number of molecules in the dengue virus

// Now we need to upload the file. This is going to require some work from the HTML.
file_load = document.getElementById("pdb")
file_load.addEventListener("change", () => {
    let fr = new FileReader()
    fr.onload = () => {
        let val = fr.result.split("\n").filter(x => {
            return x.slice(0, 4) == "ATOM"
        }) // The (async) result of loading the file, filtered by atom(takes out header, remark lines, etc).
        for(let i = 0; i < val.length; i++) {
            molecules.push(new Molecule(val[i]))
            if(!molecules[molecules.length - 1].is_antigen_chain) {
                // Translate the molecule away from the big antigen
                molecules[molecules.length - 1].translate(-50, -50, -50)
            } else {
                // Change average point
                avgPoint[0] += molecules[molecules.length - 1].x
                avgPoint[1] += molecules[molecules.length - 1].y
                avgPoint[2] += molecules[molecules.length - 1].z
                num_antigen++
            }
            // Have to render after translation because we're modifying this.x and this.y
            molecules[molecules.length - 1].render()
            molecules[molecules.length - 1].update()
            console.log(molecules[molecules.length - 1].THREE_mol.position)
        }
        avgPoint = avgPoint.map(x => {return x / num_antigen}) // Divide the sum of all the points by the number of points we have(AKA average)
    }
    fr.readAsText(file_load.files[0])
})

// Getting some light
const ambient_light = new THREE.AmbientLight(0xffffff, 0.3),
point_light = new THREE.DirectionalLight(0xffffff, 0.5)
scene.add(ambient_light)
scene.add(point_light)

// Making the scene ALIVE with animation
let center, ang = 0;
const animate = () => {
    requestAnimationFrame(animate)
    renderer.render(scene, camera)
    // Center will be our first attempt to applyImpulse.
    // force = mesh1.position.clone().negate().normalize().multiplyScalar(0.2)
    // Update antibody molecules
    for(let i = 0; i < molecules.length; i++) {
        if(!molecules[i].is_antigen_chain) {
            // Update
            molecules[i].applyForce([0, 0, 0])
            molecules[i].update()
        }
    }
    center = new THREE.Vector3()

    world.step()
}
animate()