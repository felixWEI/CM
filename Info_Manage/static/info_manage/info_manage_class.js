$(document).ready(function () {
	t = $('#table_course').DataTable({
        dom: 'Bfrtip',
        buttons: [ {
            extend: 'excelHtml5',
            customize: function( xlsx ) {
                var sheet = xlsx.xl.worksheets['sheet1.xml'];
                $('row c[r^="C"]', sheet).attr( 's', '2' );
            }
        } ]
	});

    $('#table_course tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            t.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );

    $('#delete').click( function () {
        course_id = t.row('.selected').data()[0];
        console.log(course_id)
        t.row('.selected').remove().draw( false );
        $.ajax({
            type: 'POST',
            url: '/class_delete_one_row/',
            data: {'course_id': course_id},
            dataType: 'json',
            success: function(result){
                alert('Pass');
            },
            error: function(){
                alert('Delete fail');
            }
        })

    } );

    $('#edit_teacher_info').click( function(){
        teacher_code = document.getElementById('teacher_code_2').value
        teacher_name = document.getElementById('teacher_name_2').value
        time_first_season = document.getElementById('time_first_season_2').value
        time_second_season = document.getElementById('time_second_season_2').value
        class_order = document.getElementById('class_order_2').value
        t.row('.selected').data([teacher_code, teacher_name, time_first_season, time_second_season, class_order]).draw();
    });

	$('#check_table').click( function(){

	    var table_info = t.rows().data();
	    var table_str = JSON.stringify(table_info);
	    $.ajax({
            type: 'POST',
            url: '/teacher_save_and_config/',
            data: {"teacher_table": table_str},
            dataType: "json",
            success: function(result){
                alert('Yes');
            },
            error: function (){
                alert('No');
            }

	    })

	});
    initFileInput("excelFile","/class_table_upload/")
});
function add_course_info(length){
    if (String(document.getElementById('a_0').value) in t.column(0).data()){
        alert('Teacher Id already exist!!');
        return
    }
    row_data = Array();
    for (var i=0; i < Number(length); i++ ){
        if ( document.getElementById('a_'+String(i)).value !== undefined ){
            row_data[i] = document.getElementById('a_'+String(i)).value;
            if (i==0){
                row_data[i] = row_data[i].toUpperCase();
            }
        }else{
            row_data[i] = "";
        }
//        console.log(document.getElementById(i).value);
    }
    t.row.add(row_data).draw();
    var row_str = JSON.stringify(row_data);
    $.ajax({
        type: 'POST',
            url:'/class_save_one_row/',
            data: {"row_data": row_str},
            dataType: "json",
            success: function (result) {
                alert('success');
            },
            error: function () {
                alert('fail');
            }

    })
}
function edit_course_info(){
    if ( t.row('.selected').length === 0 ){
        return
    }
    document.getElementById('e_0').value = t.row('.selected').data()[0];
    document.getElementById('e_1').value = t.row('.selected').data()[1];

    document.getElementById('e_2').innerHTML = '<option>'+t.row('.selected').data()[2]+'</option>'+document.getElementById('e_2').innerHTML;
    document.getElementById('e_3').innerHTML = '<option>'+t.row('.selected').data()[3]+'</option>'+document.getElementById('e_3').innerHTML;
    document.getElementById('e_4').value = t.row('.selected').data()[4];
    document.getElementById('e_5').innerHTML = '<option>'+t.row('.selected').data()[5]+'</option>'+document.getElementById('e_5').innerHTML;
    document.getElementById('e_6').innerHTML = '<option>'+t.row('.selected').data()[6]+'</option>'+document.getElementById('e_6').innerHTML;
    document.getElementById('e_7').innerHTML = '<option>'+t.row('.selected').data()[7]+'</option>'+document.getElementById('e_7').innerHTML;
    document.getElementById('e_8').value = t.row('.selected').data()[8];
    document.getElementById('e_9').value = t.row('.selected').data()[9];
    document.getElementById('e_10').value = t.row('.selected').data()[10];
	t_teacher_edit = $('#e_11').DataTable({
	    dom: '<"top">rt<"bottom"><"clear">',
	    "searching": false,
        "ordering": false,
        "data": [[t.row('.selected').data()[11]]]
	});

}
function submit_edit_info(){
    row_data = Array();
    for (var i=0; i < 12; i++ ){
        if ( document.getElementById('e_'+String(i)).value !== undefined ){
            row_data[i] = document.getElementById('e_'+String(i)).value;
            if (i==0){
                row_data[i] = row_data[i].toUpperCase();
            }
        }else{
            row_data[i] = "";
        }
//        console.log(document.getElementById(i).value);
    }
    t.row('.selected').data(row_data).draw();
    var row_str = JSON.stringify(row_data);
    $.ajax({
        type: 'POST',
            url:'/class_save_one_row/',
            data: {"row_data": row_str},
            dataType: "json",
            success: function (result) {
                alert('success');
            },
            error: function () {
                alert('fail');
            }

    })

}
function submit_request(){
    course_id = document.getElementById('e_0').value;
    $.ajax({
        type: 'POST',
            url:'/teacher_request_course/',
            data: {"course_id": course_id},
            dataType: "json",
            success: function (result) {
                alert('success');
            },
            error: function () {
                alert('fail');
            }

    })
}
function initFileInput(ctrlName, uploadUrl) {
    var control = $('#' + ctrlName);
    control.fileinput({
        language: 'zh', //设置语言
        uploadUrl: uploadUrl, //上传的地址
        uploadAsync: true, //默认异步上传
        showCaption: true,//是否显示标题
        showUpload: true, //是否显示上传按钮
        browseClass: "btn btn-primary", //按钮样式
        allowedFileExtensions: ["xls", "xlsx", 'txt'], //接收的文件后缀
        maxFileCount: 1,//最大上传文件数限制
        previewFileIcon: '<i class="glyphicon glyphicon-file"></i>',
        showPreview: true, //是否显示预览
        previewFileIconSettings: {
            'docx': '<i ass="fa fa-file-word-o text-primary"></i>',
            'xlsx': '<i class="fa fa-file-excel-o text-success"></i>',
            'xls': '<i class="fa fa-file-excel-o text-success"></i>',
            'pptx': '<i class="fa fa-file-powerpoint-o text-danger"></i>',
            'jpg': '<i class="fa fa-file-photo-o text-warning"></i>',
            'pdf': '<i class="fa fa-file-archive-o text-muted"></i>',
            'zip': '<i class="fa fa-file-archive-o text-muted"></i>',
        },
        uploadExtraData: function () {
            var extraValue = "test";
            return {"excelType": extraValue};
        }
    });
}

$("#excelFile").on("fileuploaded", function (event, data, previewId, index) {
    console.log(data);
    if(data.response.success == true)
    {
        alert(data.files[index].name + "上传成功!");
    //关闭
        $(".close").click();
    }
    else{
        alert(data.files[index].name + "上传失败!" + data.response.message);
    //重置
    $("#excelFile").fileinput("clear");
    $("#excelFile").fileinput("reset");
    $('#excelFile').fileinput('refresh');
    $('#excelFile').fileinput('enable');
    }
});