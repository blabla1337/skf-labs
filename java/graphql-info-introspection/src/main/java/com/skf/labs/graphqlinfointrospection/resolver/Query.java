package com.skf.labs.graphqlinfointrospection.resolver;

import graphql.kickstart.tools.GraphQLQueryResolver;

import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

import com.skf.labs.graphqlinfointrospection.entity.Post;
import com.skf.labs.graphqlinfointrospection.entity.User;
import com.skf.labs.graphqlinfointrospection.entity.UserInfo;
import com.skf.labs.graphqlinfointrospection.repository.PostRepository;
import com.skf.labs.graphqlinfointrospection.repository.UserInfoRepository;
import com.skf.labs.graphqlinfointrospection.repository.UserRepository;

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

    public UserInfo singleUserInjection(int userID){
        String sql = "SELECT id, name, surname, date_of_birth, api_key, user_id FROM user_info WHERE user_id = " + userID;
        List<UserInfo> usersInfo = jdbcTemplate.query(sql, (resultSet, rowNum) -> new UserInfo(resultSet.getInt("id"),resultSet.getString("name"), resultSet.getString("surname"),resultSet.getString("date_of_birth"),resultSet.getString("api_key"),(new User(resultSet.getInt("user_id")))));
        return usersInfo.get(0);
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
