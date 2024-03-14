import { resolve } from "daisychain";

// the daisy-chained call
resolve
    .get_project_manager()
    .get_current_project()
    .get_media_pool()
    .import_media(['./wow.mp4', './pie.jpg']);

/* should get run sequentially as...
 * 
 *  {'fn':'resolve.get_project_manager', 
 *   'args':[], 
 *   'kwargs':{}}
 *   
 *  -> {
 *      'type': 'ProjectManager',
 *  }
 *  ... then ...
 *
 *  {'fn':'resolve.get_current_project', 
 *   'args':[], 
 *   'kwargs':{}}
 *   
 *  -> {
 *      'type': 'Project',
 *      'name': 'Captains Log'
 *  }
 *  ... then ...
 *
 *  {'fn':'get_media_pool', 
 *   'args':[], 
 *   'kwargs':{}}
 *
 *  -> {
 *      'type': 'MediaPool',
 *  }
 *  ... then ...
 *
 *  {'fn':'import_media', 
 *   'args':['./wow.mp4', './pie.jpg'], 
 *   'kwargs':{}}
 *
 *  -> [{
 *      'type': 'MediaPoolItem',
 *      'uuid': '48b51697-aeab-492e-b0af-5b10c269d9b6'
 *     },
 *     {
 *      'type': 'MediaPoolItem',
 *      'uuid': '0a79d146-b524-49e9-a322-16b39bdb4b7a'
 *     }]
 * 
*/

// shortcut for the above
pool = resolve.get_media_pool() // retain reference to the media pool
pool.import_media(["./wow.mp4", './pie.jpg'])

