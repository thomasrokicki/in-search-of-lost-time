/**
 * BUFFER_ELEMENT_SIZE - The size of a array element.
 * Used for SAB.
 * @const
 * @global
 */
const BUFFER_ELEMENT_SIZE = 64;

/**
 * CACHE_SIZE - The size of the users cache
 * It is used to build eviction sets.
 * This param needs to be modified for different systems.
 * @const
 * @global
 */
const CACHE_SIZE = 4096*4096*4;
