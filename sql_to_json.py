public JSONArray getResults() {
		String myPath = DB_PATH + DB_NAME;// Set path to your database
		SQLiteDatabase myDataBase = SQLiteDatabase.openDatabase(myPath, null, SQLiteDatabase.OPEN_READONLY);


		String searchQuery = "SELECT  * FROM ";
		Cursor cursor = myDataBase.rawQuery(searchQuery, null);

		JSONArray resultSet = new JSONArray();
		JSONObject returnObj = new JSONObject();

		cursor.moveToFirst();
		while (cursor.isAfterLast() == false) {

			int totalColumn = cursor.getColumnCount();
			JSONObject rowObject = new JSONObject();

			for (int i = 0; i < totalColumn; i++) {
				if (cursor.getColumnName(i) != null) {

					try {

						if (cursor.getString(i) != null) {
							Log.d("TAG_NAME", cursor.getString(i));
							rowObject.put(cursor.getColumnName(i), cursor.getString(i));
						} else {
							rowObject.put(cursor.getColumnName(i), "");
						}
					} catch (Exception e) {
						Log.d("TAG_NAME", e.getMessage());
					}
				}

			}

			resultSet.put(rowObject);
			cursor.moveToNext();
		}

		cursor.close();
		Log.d("TAG_NAME", resultSet.toString());
		return resultSet;
	}