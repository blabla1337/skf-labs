package com.skf.labs.ldapinjection;

import java.util.Hashtable;
import java.util.List;

import javax.naming.Context;
import javax.naming.NamingEnumeration;
import javax.naming.directory.Attribute;
import javax.naming.directory.Attributes;
import javax.naming.directory.DirContext;
import javax.naming.directory.InitialDirContext;
import javax.naming.directory.SearchControls;
import javax.naming.directory.SearchResult;


import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.beans.factory.annotation.Autowired;



@Controller
public class LdapInjectionController {
    


    @PostMapping("/login")
	public String login(@RequestParam(name="username", required=true) String username,@RequestParam(name="password", required=true) String password,Model model) throws javax.naming.NamingException{
        Hashtable env = new Hashtable();
        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
        env.put(Context.PROVIDER_URL,  "ldap://localhost:4444/dc=com");
        env.put(Context.SECURITY_AUTHENTICATION, "simple");
        env.put(Context.SECURITY_PRINCIPAL, "cn=ldapadmin,dc=com");
        env.put(Context.SECURITY_CREDENTIALS, "mysecret");

        DirContext dctx = new InitialDirContext(env);
        SearchControls sc = new SearchControls();
        String[] attributeFilter = { "cn", "sn" };

        sc.setReturningAttributes(attributeFilter);
        sc.setSearchScope(SearchControls.SUBTREE_SCOPE);

        String filter = "(&(cn="+username+")(sn="+password+"))";
        String base = "ou=accounts";

        NamingEnumeration results = dctx.search(base, filter, sc);
        boolean found = false;

        while (results.hasMore()) {
            SearchResult sr = (SearchResult) results.next();
            Attributes attrs = sr.getAttributes();
            Attribute attr = attrs.get("cn");
            if(attr.get().equals("admin")){
                found = true;
            }
        }
        dctx.close();

        if(found){
            model.addAttribute("content","You are now admin user!");
        }else{
            model.addAttribute("content","Wrong identity provided!");
        }
        return "index";
      }
}
