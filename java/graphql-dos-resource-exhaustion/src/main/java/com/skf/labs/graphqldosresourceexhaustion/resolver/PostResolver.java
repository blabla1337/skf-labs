package com.skf.labs.graphqldosresourceexhaustion.resolver;
import graphql.kickstart.tools.GraphQLResolver;
import com.skf.labs.graphqldosresourceexhaustion.entity.User;
import com.skf.labs.graphqldosresourceexhaustion.entity.Post;
import com.skf.labs.graphqldosresourceexhaustion.entity.UserInfo;
import com.skf.labs.graphqldosresourceexhaustion.repository.PostRepository;
import com.skf.labs.graphqldosresourceexhaustion.repository.UserRepository;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class PostResolver implements GraphQLResolver<Post> {
    @Autowired
    private UserRepository userRepository;

    public PostResolver(UserRepository userRepository){
        this.userRepository = userRepository;
    }

    public User user(Post post){
        return userRepository.findById(post.getUser().getId()).orElseThrow(null);
    }
    
}
