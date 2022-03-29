package com.skf.labs.graphqldosresourceexhaustion.resolver;
import graphql.kickstart.tools.GraphQLResolver;
import com.skf.labs.graphqldosresourceexhaustion.entity.User;
import com.skf.labs.graphqldosresourceexhaustion.entity.UserInfo;
import com.skf.labs.graphqldosresourceexhaustion.repository.UserRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class UserInfoResolver implements GraphQLResolver<UserInfo> {
    @Autowired
    private UserRepository userRepository;

    public UserInfoResolver(UserRepository userRepository){
        this.userRepository = userRepository;
    }

    public User user(UserInfo userInfo){
        return userRepository.findById(userInfo.getUser().getId()).orElseThrow(null);
    }
    
}
