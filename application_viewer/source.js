// Start by initializing simple THREE.js scene, camera, etc.
const scene = new THREE.Scene(),
camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
camera.position.z = 20

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

// Making a simple sphere that coordinates with OIMO and Three.js.
let mat = new THREE.MeshStandardMaterial({
    color: 0x00ff00
}),
sphere = new THREE.SphereGeometry(2),
mesh = new THREE.Mesh(sphere, mat),
sph = world.add({
    type: "sphere",
    size: [2, 2, 2],
    pos: [0, 0, 0],
    move: false,
    density: 0.01,
    friction: 0.1
})
scene.add(mesh)

let sphere1 = new THREE.SphereGeometry(1),
mesh1 = new THREE.Mesh(sphere1, mat),
sph1 = world.add({
    type: "sphere",
    size: [1, 1, 1],
    pos: [0, 10, 0],
    move: true,
    density: 1,
    friction: 2
})
scene.add(mesh1)

// Getting some light
const ambient_light = new THREE.AmbientLight(0xffffff, 0.3),
point_light = new THREE.DirectionalLight(0xffffff, 0.5)
scene.add(ambient_light)
scene.add(point_light)

// Making the scene ALIVE with animation
let center;
const animate = () => {
    requestAnimationFrame(animate)
    renderer.render(scene, camera)
    center = new THREE.Vector3()
    /**
     * How copying pos and quat work:
     * box[three.js version].position.copy(box[OIMO version].getPosition())
     * box[three.js version].quaternion.copy(box[OIMO version].getQuaternion())
     */
    mesh.position.copy(sph.getPosition())
    mesh.quaternion.copy(sph.getQuaternion())
    mesh1.position.copy(sph1.getPosition())
    mesh1.quaternion.copy(sph1.getQuaternion())
    force = mesh1.position.clone().negate().normalize().multiplyScalar(0.1)
    sph1.applyImpulse(center, force)
    // console.log(mesh.position)
    // console.log(sph1, force, mesh1.position)
    world.step()
}
animate()