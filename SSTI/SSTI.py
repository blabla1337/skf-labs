from flask import Flask, request, url_for, render_template_string

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.errorhandler(404)
def page_not_found(e):
    template = """
  <!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Live demonstrations</title>

<link href="/static/css/bootstrap.min.css" rel="stylesheet">
<link href="/static/css/datepicker3.css" rel="stylesheet">
<link href="/static/css/styles.css" rel="stylesheet">

<!--Icons-->
<script src="/static/js/lumino.glyphs.js"></script>

</head>

<body>
	<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
		<div class="container-fluid">
			<div class="navbar-header">
				<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#sidebar-collapse">
					<span class="sr-only">Toggle navigation</span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</button>
				<ul class="user-menu">
					<li class="dropdown pull-right">

						<ul class="dropdown-menu" role="menu">
						</ul>
					</li>
				</ul>
			</div>
		</div><!-- /.container-fluid -->
	</nav>

	<div id="sidebar-collapse" class="col-sm-3 col-lg-2 sidebar">
	<br/><br/>
	<center>
		<img src="/static/img/logo.svg" width="60%" height="60%"/>
		<br/>
		<p style="color:#515594; font-size:1.0em;"><a href="https://github.com/blabla1337/skf-flask" style="color:#515594; font-size:1.7em;">OWASP S.K.F.</a></p>  	 			<p><a href="https://gitter.im/Security-Knowledge-Framework/Lobby" rel="nofollow"> 				<img src="/static/img/badge.svg" alt="Join the chat at https://gitter.im/Security-Knowledge-Framework/Lobby" data-canonical-src="/static/img/badge.svg" style="max-width:100%;"></a> 			</p> 
	</center>
	</div><!--/.sidebar-->

	<div class="col-sm-9 col-sm-offset-3 col-lg-10 col-lg-offset-2 main">
		<div class="row">

		</div><!--/.row-->

		<div class="row">
			<div class="col-lg-12">
				<h1 class="page-header">Live demonstration!</h1>
			</div>
		</div><!--/.row-->


		<div class="row">
			<div class="col-lg-12">
				<div class="panel panel-default">
					<div class="panel-heading">Server side template injection!</div>
					<div class="panel-body">
						<div class="col-md-6">
							{0}
               			</div>
						</form>
					</div>
				</div>
			</div><!-- /.col-->
		</div><!-- /.row -->

     <center> <p style="font-size:2em;">   </p></center>

	</div><!--/.main-->

	<script src="/static/js/jquery-1.11.1.min.js"></script>
	<script src="/static/js/bootstrap.min.js"></script>
	<script src="/static/js/chart.min.js"></script>
	<script src="/static/js/chart-data.js"></script>
	<script src="/static/js/easypiechart.js"></script>
	<script src="/static/js/easypiechart-data.js"></script>
	<script src="/static/js/bootstrap-datepicker.js"></script>

	</script>
</body>

</html>

""".format(request.url)
    return render_template_string(template), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')
