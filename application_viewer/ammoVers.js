const Ammo = require("./ammo");
// Working from this guide: https://medium.com/@bluemagnificent/intro-to-javascript-3d-physics-using-ammo-js-and-three-js-dd48df81f591

// Create physics world
let physicsWorld;
const setupPhysicsWorld = () => {
    let collisionConfiguration = new Ammo.btDefaultCollisionConfiguration(),
    dispater = new Ammo.btCollisionDispatcher(collisionConfiguration),
    overlappingPairCache = new Ammo.btDbvtBroadphase(),
    solver = new Ammo.btSequentialImpulseConstrainstSolver()

    physicsWorld = new Ammo.btDiscreteDynamicsWorld(dispatcher, overlappingPairCache)
    physicsWorld.setGravity(new Ammo.btVector3(0, -10, 0))
}