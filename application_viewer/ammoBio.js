/**
 * Steps:
 * Initialize Ammo.js(setupPhysicsWorld)
 * Initialize THREE.js(setupGraphics)
 * Load the PDB file(loadPDB)
 * Identify which chains are light, heavy, and not a part of the antibody(will be assumed to be a part of the antigen)(detectChains)
 * Render them
 * Group them together(initially attempt with joints, if it doesn't work move on to creating custom meshes)
 * Pull them towards the epitopes(initially explicitly specify)
 * Create a genetic algorithm
 */