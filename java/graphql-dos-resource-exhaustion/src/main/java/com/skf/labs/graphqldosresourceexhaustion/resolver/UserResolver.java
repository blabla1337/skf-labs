package com.skf.labs.graphqldosresourceexhaustion.resolver;
import graphql.kickstart.tools.GraphQLResolver;
import com.skf.labs.graphqldosresourceexhaustion.entity.User;
import com.skf.labs.graphqldosresourceexhaustion.entity.Post;
import com.skf.labs.graphqldosresourceexhaustion.entity.UserInfo;
import com.skf.labs.graphqldosresourceexhaustion.repository.PostRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class UserResolver implements GraphQLResolver<User> {
    @Autowired
    private PostRepository postRepository;

    public UserResolver(PostRepository postRepository){
        this.postRepository = postRepository;
    }

    public Post post(User user){
        return postRepository.findById(user.getPost().getId()).orElseThrow(null);
    }
    
}
