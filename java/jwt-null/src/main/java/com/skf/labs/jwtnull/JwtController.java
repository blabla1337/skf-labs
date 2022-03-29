package com.skf.labs.jwtnull;

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
import java.util.Base64;
import java.lang.*;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTCreationException;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.exceptions.JWTVerificationException;
import com.auth0.jwt.interfaces.DecodedJWT;

import com.skf.labs.jwtnull.JwtModel;
import com.skf.labs.jwtnull.User;

@Controller
public class JwtController {
    @PostMapping(value = "/auth", consumes = "application/json", produces = "application/json")
    public ResponseEntity<Object> auth(@RequestBody String req) {
        JSONObject jObject = new JSONObject(req);
        User user = JwtModel.users.stream().filter(u -> u.getUsername().equals(jObject.get("username"))).findFirst()
                .orElse(null);

        if (null != user && user.getPassword().equals(jObject.get("password"))) {

            Algorithm algorithm = Algorithm.HMAC256("VerylongUnbreakablesecretbecausebruteforceisnotthecase");
            String token = JWT.create()
                    .withClaim("identity", user.getId())
                    .sign(algorithm);

            JSONObject jwtObj = new JSONObject();
            jwtObj.put("access_token", token);

            return ResponseEntity.status(HttpStatus.OK).body(jwtObj.toMap());

        } else {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body("FORBIDDEN");
        }
    }

    @GetMapping("/protected")
    public ResponseEntity<Object> protectedPage(@RequestHeader("Authorization") String jwtToken) {
        jwtToken = jwtToken.substring(4);
        String jwtHeader = jwtToken.split("\\.")[0];
        byte[] decodedBytes = Base64.getDecoder().decode(jwtHeader);
        jwtHeader = new String(decodedBytes);
        JSONObject jwtHeaderObj = new JSONObject(jwtHeader);
        Algorithm algorithm = Algorithm.HMAC256("VerylongUnbreakablesecretbecausebruteforceisnotthecase");
        if (jwtHeaderObj.get("alg").equals("none")) {
            algorithm = Algorithm.none();
        }
        try {
            JWTVerifier verifier = JWT.require(algorithm).build();
            DecodedJWT decodedJWT = verifier.verify(jwtToken);
            User user = JwtModel.users.stream()
                    .filter(u -> u.getId() == Integer.parseInt(decodedJWT.getClaims().get("identity").toString()))
                    .findFirst().orElse(null);
            if (null != user) {
                JSONObject jsonObj = new JSONObject();
                jsonObj.put("id", user.getId());
                jsonObj.put("username", user.getUsername());
                jsonObj.put("username", user.getRole());
                return ResponseEntity.status(HttpStatus.OK).body(jsonObj.toMap());
            } else {
                return ResponseEntity.status(HttpStatus.FORBIDDEN).body("FORBIDDEN");
            }
        } catch (JWTVerificationException e) {
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body("FORBIDDEN");
        }
    }
}
