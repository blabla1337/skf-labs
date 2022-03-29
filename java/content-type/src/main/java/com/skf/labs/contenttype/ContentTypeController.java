package com.skf.labs.contenttype;


import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.json.JSONObject;
import org.json.JSONException;
import javax.servlet.http.HttpServletResponse;



@Controller
public class ContentTypeController {
    @PostMapping("/unprotected")
	public ResponseEntity<Object> rUnprotected(@RequestParam(name="no_header", required=true) String name) {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("key",name);
        jsonObject.put("key2","another value");

        return ResponseEntity.status(HttpStatus.OK).body(jsonObject.toString());
	}

    @PostMapping(value="/protected",produces = "application/json")
	public ResponseEntity<Object> rProtected(@RequestParam(name="with_header", required=true) String name, HttpServletResponse response) {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("key",name);
        jsonObject.put("key2","another value");
        response.addHeader("Content-Type","application/json");

        return ResponseEntity.status(HttpStatus.OK).body(jsonObject.toString());
	}
    
}
