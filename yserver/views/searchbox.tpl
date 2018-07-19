% from bottle import request
  <div class="searchbox">
  <form method="GET" action="/search">
  <input type='text' name='search' id='search' value='{{request.query.search}}'></input>
  <input type='submit' value='Rechercher' id='search'></input>
  </form>
  </div>
%end

