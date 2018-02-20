$(document).ready(function () {
	t = $('#table_teacher').DataTable({
        dom: 'Bfrtip',
        buttons: [ {
            extend: 'excelHtml5',
            customize: function( xlsx ) {
                var sheet = xlsx.xl.worksheets['sheet1.xml'];
                $('row c[r^="C"]', sheet).attr( 's', '2' );
            }
        } ]
	});

    $('#table_teacher tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            t.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );

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
        t.row('.selected').remove().draw( false );
    } );

	$('#edit_table').click( function(){
        if ( t.row('.selected').length === 0 ){
            return
        }
        console.log(t.row('.selected').data());
        document.getElementById('0').value = t.row('.selected').data()[0];
        document.getElementById('1').value = t.row('.selected').data()[1];
        document.getElementById('2').value = t.row('.selected').data()[2];
        document.getElementById('3').value = t.row('.selected').data()[3];
        document.getElementById('4').value = t.row('.selected').data()[4];
        document.getElementById('5').value = t.row('.selected').data()[5];
	});

    $('#edit_teacher_info').click( function(){
        teacher_code = document.getElementById('teacher_code_2').value
        teacher_name = document.getElementById('teacher_name_2').value
        time_first_season = document.getElementById('time_first_season_2').value
        time_second_season = document.getElementById('time_second_season_2').value
        class_order = document.getElementById('class_order_2').value
        t.row('.selected').data([teacher_code, teacher_name, time_first_season, time_second_season, class_order]).draw();
    });

	$('#add_teacher_info').on('click',function(){
        if (document.getElementById('teacher_code').value in t.column(0).data()){
            alert('Teacher Id already exist!!');
            return
        }
	    t.row.add([
            document.getElementById('teacher_code').value,
            document.getElementById('teacher_name').value,
            document.getElementById('time_first_season').value,
            document.getElementById('time_second_season').value,
            document.getElementById('class_order').value,
	    ]).draw();
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

//	$('#submit_file').click( function() {
//	    file = document.getElementById('InputFile').value;
//	    initFileInput('InputFile', file)
//	    console.log(file);
//	})
    initFileInput("excelFile","/teacher_table_upload/")
});

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