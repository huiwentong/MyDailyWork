// change the position X of all layers with random number
var project_root = "E:/AEscriptTest"; // 这是你的图片路径
var outPut_root = "E:/AEscriptTest/out"; // 这是你的输出路径
// var myComp = app.project.activeItem;
// var x = 0;
// for (var i = 1; i <= myComp.numLayers; i++) {
//   // If you use Math.random(), this does not work
//   // x = 400 * (Math.random()) – 200;
//   // use new generateRandomNumber() instead

//   x = 400 * generateRandomNumber() - 200;
//   var currentPos = myComp.layer(i).property("Position").value;
//   myComp.layer(i).property("Position").setValue([currentPos[0] + x, currentPos[1]]);
// }
// alert(app.buildName);
// myComp.fram
function Add_png_to_comp(map_item, parent) {
    this.width = map_item[0].width;
    this.height = map_item[0].height;
    this.name = map_item[0].name.replace('.png', '');
    this.comp = parent.items.addComp(this.name, this.width, this.height, 1.0, 0.04, 25);
    this.upLayer = this.comp.layers.add(map_item[0]);
    this.downLayer = this.comp.layers.add(map_item[1]);
    this.upLayer.trackMatteType = TrackMatteType.LUMA;
    this.fileName = new File(this.name);
    var ModuleSetting = {
        // "Format": "PNG Sequence",
        // "Channels": "RGB + Alpha",
        // "Crop": true,
        "Output File Info": {
            "Full Flat Path": outPut_root + '/' + File.decode('out_'+this.name)
        }
        // "Output To": FF + "/out/out" + this.name
    };
    this.renderItem = app.project.renderQueue.items.add(this.comp);
    // alert(this.renderItem.outputModule(1).templates);
    this.renderItem.outputModule(1).setSettings(ModuleSetting);
    try{
        this.renderItem.outputModule(1).applyTemplate("PNG");
    }
    catch (err){
        this.renderItem.outputModule(1).applyTemplate("HWT");
    }
    // ModuleSetting = this.renderItem.outputModule(1).getSettings( GetSettingsFormat.STRING_SETTABLE );
}

var FF = new Folder(project_root);
// 文件夹遍历加判断
function folder_recursive(folderGroup) {
    // 获取文件夹所有文件
    var files = folderGroup.getFiles();
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        if (String(file).split('.')[1] === 'png' || String(file).split('.')[1] === 'jpg' || 
        String(file).split('.')[1] === 'PNG' || String(file).split('.')[1] === 'JPG'){
            //判断是否是png，jpg，PNG，JPG
            app.project.importFile(new ImportOptions(new File(String(file))));
        }
    }
}

folder_recursive(FF);

var map = new Object()
var folder = app.project.items.addFolder("脚本导入png");
var total = app.project.items.length;
var footagePngList = [];

for (var i=1; i<total; i++){
    if(app.project.item(i).name.match('png') && app.project.item(i).typeName === "Footage"){
        footagePngList.push(app.project.item(i));
    }
}
for (var i=0;i<footagePngList.length;i++){
    footagePngList[i].parentFolder = folder;
    if(footagePngList[i].name.match("_alpha")){
        for(var j=0;j<footagePngList.length;j++){
            if(footagePngList[i].name.replace('_alpha', '') === footagePngList[j].name){
                map[footagePngList[j].name] = [footagePngList[j], footagePngList[i]];
                break;
            }
        }
    }
}
var compFolder = app.project.items.addFolder("脚本comp");
for(var item in map){
    var comp_util = new Add_png_to_comp(map[item],compFolder);
     
}
// for(var i=0;i<map.length;i++){
// compFolder.items.addComp('asd', 400,400,1,25,25);
// var test = new Add_png_to_comp(map['s_s_fs0.png'],compFolder);
