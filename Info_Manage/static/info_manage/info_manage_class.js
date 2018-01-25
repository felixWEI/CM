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
        t.row('.selected').remove().draw( false );
    } );

	$('#edit_table').click( function(){
        if ( t.row('.selected').length === 0 ){
            return
        }
        document.getElementById('teacher_code_2').value = t.row('.selected').data()[0];
        document.getElementById('teacher_name_2').value = t.row('.selected').data()[1];
        document.getElementById('time_first_season_2').value = t.row('.selected').data()[2];
        document.getElementById('time_second_season_2').value = t.row('.selected').data()[3];
        document.getElementById('class_order_2').value = t.row('.selected').data()[4];
	});

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

	})
});
function add_course_info(length){
    if (String(document.getElementById('0').value) in t.column(0).data()){
        alert('Teacher Id already exist!!');
        return
    }
    row_data = Array();
    for (var i=0; i < Number(length); i++ ){
        if ( document.getElementById(String(i)).value !== undefined ){
            row_data[i] = document.getElementById(String(i)).value;
        }else{
            row_data[i] = "";
        }
//        console.log(document.getElementById(i).value);
    }
    t.row.add(row_data).draw();
    var row_str = JSON.stringify(row_data);
    console.log(row_str);
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