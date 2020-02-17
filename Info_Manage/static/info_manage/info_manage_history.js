$(document).ready(function () {
	t = $('#table_course_personal').DataTable({
        dom: 'Blfrtip',
        lengthMenu: [50,100],
        buttons: []
	});

    $('#table_course_personal tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            t.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );
    $('#e_11 tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            t.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );
});
function submit_select_info(){
    var year = document.getElementById('history_year_select').value;
    $.ajax({
        type: 'POST',
        url: '/history_search_by_year/',
        data: {'year': year},
        dataType: "json",
        success: function(result){
            console.log(result['init_data'])
            document.getElementById('current_year').innerText = result['init_data'][0]
            $('#table_course_personal').DataTable().clear();
            for (var i = 0; i < result['class_table'].length; i++){
                $('#table_course_personal').DataTable().row.add(result['class_table'][i])
            }
            $('#table_course_personal').DataTable().draw();
        },
        error: function (){
            alert('获取历史排课信息失败');
        }
    });
}

function export_course_info(){
    current_year = document.getElementById('current_year').innerText;
    var post_url = '/history_export_report/?current_year='+current_year;
    location.replace(post_url);
}
function export_teacher_info(){
    current_year = document.getElementById('current_year').innerText;
    var post_url = '/history_export_teacher/?current_year='+current_year;
    location.replace(post_url);
}
//function initFileInput(ctrlName, uploadUrl) {
//    var control = $('#' + ctrlName);
//    control.fileinput({
//        language: 'zh', //设置语言
//        uploadUrl: uploadUrl, //上传的地址
//        uploadAsync: true, //默认异步上传
//        showCaption: true,//是否显示标题
//        showUpload: true, //是否显示上传按钮
//        browseClass: "btn btn-primary", //按钮样式
//        allowedFileExtensions: ["xls", "xlsx", 'txt'], //接收的文件后缀
//        maxFileCount: 1,//最大上传文件数限制
//        previewFileIcon: '<i class="glyphicon glyphicon-file"></i>',
//        showPreview: true, //是否显示预览
//        previewFileIconSettings: {
//            'docx': '<i ass="fa fa-file-word-o text-primary"></i>',
//            'xlsx': '<i class="fa fa-file-excel-o text-success"></i>',
//            'xls': '<i class="fa fa-file-excel-o text-success"></i>',
//            'pptx': '<i class="fa fa-file-powerpoint-o text-danger"></i>',
//            'jpg': '<i class="fa fa-file-photo-o text-warning"></i>',
//            'pdf': '<i class="fa fa-file-archive-o text-muted"></i>',
//            'zip': '<i class="fa fa-file-archive-o text-muted"></i>',
//        },
//        uploadExtraData: function () {
//            var extraValue = "test";
//            return {"excelType": extraValue};
//        }
//    });
//}

//$("#excelFile").on("fileuploaded", function (event, data, previewId, index) {
//    console.log(data);
//    if(data.response.result == 'Pass')
//    {
//        alert(data.files[index].name + "上传成功!");
//    //关闭
//        $(".close").click();
//    }
//    else{
//        alert(data.files[index].name + "上传失败!" + data.response.message);
//    //重置
//    $("#excelFile").fileinput("clear");
//    $("#excelFile").fileinput("reset");
//    $('#excelFile').fileinput('refresh');
//    $('#excelFile').fileinput('enable');
//    }
//})