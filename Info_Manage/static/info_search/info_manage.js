$(document).ready(function () {
	t = $('#table_teacher').DataTable();

    $('#table_teacher tbody').on( 'click', 'tr', function () {
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
	    console.log(t.row('.selected').data());

        document.getElementById('teacher_code_2').value = t.row('.selected').data()[0];
        document.getElementById('teacher_name_2').value = t.row('.selected').data()[1];
        document.getElementById('time_first_season_2').value = t.row('.selected').data()[2];
        document.getElementById('time_second_season_2').value = t.row('.selected').data()[3];
        document.getElementById('class_order_2').value = t.row('.selected').data()[4];
	});

	$('#add_teacher_info').on('click',function(){
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

	})
});