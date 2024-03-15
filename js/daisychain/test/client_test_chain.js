import { resolve } from "daisychain";

console.log(resolve);
// the daisy-chained call
// pool = (resolve
//     .get_project_manager()
//     .get_current_project()
//     .get_media_pool())
//     // .import_media(['./wow.mp4', './pie.jpg']);
//
// console.log('got pool:', pool)
//
// shortcut for the above
//pool = resolve.get_media_pool() // retain reference to the media pool
//pool.import_media(["./wow.mp4", './pie.jpg'])

