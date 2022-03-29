package com.skf.labs.graphqlinjections.resolver;

import graphql.kickstart.tools.GraphQLQueryResolver;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.TimeUnit;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

import com.skf.labs.graphqlinjections.entity.Post;
import com.skf.labs.graphqlinjections.entity.User;
import com.skf.labs.graphqlinjections.entity.UserInfo;
import com.skf.labs.graphqlinjections.repository.PostRepository;
import com.skf.labs.graphqlinjections.repository.UserInfoRepository;
import com.skf.labs.graphqlinjections.repository.UserRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.jdbc.core.JdbcTemplate;


@Component
public class Query implements GraphQLQueryResolver{
    private UserRepository userRepository;
    private UserInfoRepository userInfoRepository;
    private PostRepository postRepository;
    @PersistenceContext
    private EntityManager em;
    @Autowired
    private JdbcTemplate jdbcTemplate;  

    @Autowired
    public Query(UserRepository userRepository, UserInfoRepository userInfoRepository, PostRepository postRepository){
        this.userRepository = userRepository;
        this.userInfoRepository = userInfoRepository;
        this.postRepository = postRepository;
    }
    
    public Iterable<User> findAllUsers(){
        return userRepository.findAll();
    }

    public UserInfo singleUser(int userID){
        return (UserInfo)userInfoRepository.findById(userID).orElseThrow(null);
    }

    public User getUser(String username){
        String sql = "SELECT id, username, admin FROM user WHERE username = '" + username + "'";
        List<User> users = jdbcTemplate.query(sql, (resultSet, rowNum) -> new User(resultSet.getInt("id"),resultSet.getString("username"), resultSet.getBoolean("admin")));
        return users.get(0);
    }

    public boolean isSqlUp(String ip) throws IOException, InterruptedException{
        String sIp[] = ip.split(":");
        Process pb = new ProcessBuilder("/bin/sh", "-c","nc -w 3 "+ sIp[0]+" "+ sIp[1]).redirectErrorStream(true).start();
        pb.waitFor(5, TimeUnit.SECONDS);
        if(pb.exitValue() == 0) return true;
        return false;
    }

    public Iterable<UserInfo> findAllUserInfos(){
        return userInfoRepository.findAll();
    }

    public Iterable<Post> findAllPosts(){
        return postRepository.findAll();
    }

    public long countUsers(){
        return userRepository.count();
    }
    public long countUserInfos(){
        return userInfoRepository.count();
    }

    public long countPosts(){
        return postRepository.count();
    }
}
