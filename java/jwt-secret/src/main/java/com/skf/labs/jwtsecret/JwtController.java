package com.skf.labs.jwtsecret;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestHeader;

import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;

import org.json.JSONObject;
import org.json.JSONException;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTCreationException;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.exceptions.JWTVerificationException;
import com.auth0.jwt.interfaces.DecodedJWT;

import com.skf.labs.jwtsecret.JwtModel;
import com.skf.labs.jwtsecret.User;


@Controller
public class JwtController {
    @PostMapping(value="/auth", 
                 consumes = "application/json", 
                 produces = "application/json")
	public ResponseEntity<Object> auth(@RequestBody String req) {
        JSONObject jObject = new JSONObject(req);
         User user =  JwtModel.users.stream().filter(u -> u.getUsername().equals(jObject.get("username"))).findFirst().orElse(null);
       
           if(null!= user && user.getPassword().equals(jObject.get("password"))){

           Algorithm algorithm = Algorithm.HMAC256("secret");
            String token = JWT.create()
                                .withClaim("identity",user.getId())
                                .sign(algorithm);

                JSONObject jwtObj = new JSONObject();
                jwtObj.put("access_token",token);
       
                return ResponseEntity.status(HttpStatus.OK).body(jwtObj.toMap());
           
       }else{
        return ResponseEntity.status(HttpStatus.FORBIDDEN).body("FORBIDDEN"); 
       }
	}

    @GetMapping("/protected")
    public  ResponseEntity<Object> protectedPage(@RequestHeader("Authorization") String jwtToken){
        jwtToken = jwtToken.substring(4);
        Algorithm algorithm = Algorithm.HMAC256("secret");
        try{
            JWTVerifier verifier = JWT.require(algorithm).build();
            DecodedJWT decodedJWT = verifier.verify(jwtToken);

            User user =  JwtModel.users.stream().filter(u -> u.getId() == Integer.parseInt(decodedJWT.getClaims().get("identity").toString())).findFirst().orElse(null);
            if(null != user){
                JSONObject jsonObj = new JSONObject();
                jsonObj.put("id",user.getId());
                jsonObj.put("username",user.getUsername());
                return ResponseEntity.status(HttpStatus.OK).body(jsonObj.toMap());
            }else{
                return ResponseEntity.status(HttpStatus.FORBIDDEN).body("FORBIDDEN"); 
            }
        }catch(JWTVerificationException e){
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body("FORBIDDEN"); 
        }
   }
}
